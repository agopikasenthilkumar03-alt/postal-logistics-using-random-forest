from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.security import ROLE_ADMIN, ROLE_STAFF, require_role
from app.db.session import get_db
from app.models.post import Post
from app.models.prediction import AdminApproval, DelayPrediction, SmsLog
from app.models.weather import WeatherSnapshot
from app.schemas.prediction import ApprovalCreate, ApprovalRead, PredictionRead
from app.schemas.weather import WeatherRead
from app.services.prediction_service import get_model_with_fallback, predict_delay
from app.services.sms_service import build_delay_message, send_sms
from app.services.weather_service import fetch_weather_for_office

router = APIRouter(prefix="/predictions", tags=["predictions"])


class PredictionRunRequest(BaseModel):
    post_id: str
    route_distance: float
    historical_delivery_time: float
    month: int
    use_forecast: bool = True


@router.post("/run", response_model=PredictionRead, dependencies=[Depends(require_role({ROLE_ADMIN, ROLE_STAFF}))])
def run_prediction(payload: PredictionRunRequest, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == payload.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    weather_payload = fetch_weather_for_office(post.source_post_office)
    weather_payload.forecast_window = "forecast_24h" if payload.use_forecast else "current"
    weather = WeatherSnapshot(**weather_payload.dict())
    db.add(weather)
    db.commit()
    db.refresh(weather)

    weather_read = WeatherRead.from_orm(weather)
    model = get_model_with_fallback("backend/data/sample_delivery_history.csv")
    predicted_delay, predicted_days = predict_delay(
        model,
        payload.route_distance,
        payload.historical_delivery_time,
        weather_read,
        payload.month,
    )

    prediction = DelayPrediction(
        post_id=post.id,
        weather_snapshot_id=weather.id,
        predicted_delay=predicted_delay,
        predicted_delay_days=predicted_days,
        model_version=model.model_version,
        created_at=datetime.utcnow(),
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("", response_model=list[PredictionRead], dependencies=[Depends(require_role({ROLE_ADMIN}))])
def list_predictions(db: Session = Depends(get_db)):
    return db.query(DelayPrediction).all()


@router.get("/pending", response_model=list[PredictionRead], dependencies=[Depends(require_role({ROLE_ADMIN}))])
def list_pending_predictions(db: Session = Depends(get_db)):
    return (
        db.query(DelayPrediction)
        .outerjoin(AdminApproval, DelayPrediction.id == AdminApproval.prediction_id)
        .filter(AdminApproval.id.is_(None))
        .all()
    )


@router.post("/{prediction_id}/approval", response_model=ApprovalRead, dependencies=[Depends(require_role({ROLE_ADMIN}))])
def approve_prediction(prediction_id: int, payload: ApprovalCreate, db: Session = Depends(get_db)):
    prediction = db.query(DelayPrediction).filter(DelayPrediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    if prediction.approval:
        raise HTTPException(status_code=409, detail="Prediction already reviewed")

    approval = AdminApproval(
        prediction_id=prediction.id,
        approved=payload.approved,
        approved_by=payload.approved_by,
        approved_at=datetime.utcnow(),
        remarks=payload.remarks,
    )
    db.add(approval)

    if payload.approved and prediction.predicted_delay:
        post = prediction.post
        message = build_delay_message(prediction.predicted_delay_days)
        for phone in [post.sender_phone, post.receiver_phone]:
            response = send_sms(phone, message)
            log = SmsLog(
                post_reference=post.post_id,
                phone_number=phone,
                message_body=message,
                sent_at=datetime.utcnow(),
                provider_reference=response.get("provider_reference"),
            )
            db.add(log)

    db.commit()
    db.refresh(approval)
    return approval
