from datetime import datetime

from app.ml.random_forest import FEATURES, SimpleRandomForest, load_or_train_model
from app.schemas.weather import WeatherRead


FLOOD_RISK_MAP = {"Low": 0.0, "Medium": 0.5, "High": 1.0}


def _features_from_inputs(
    route_distance: float,
    historical_delivery_time: float,
    weather: WeatherRead,
    month: int,
) -> dict[str, float]:
    return {
        "route_distance": route_distance,
        "historical_delivery_time": historical_delivery_time,
        "rainfall": weather.rainfall_intensity,
        "wind_speed": weather.wind_speed,
        "temperature": weather.temperature,
        "flood_risk": FLOOD_RISK_MAP.get(weather.flood_risk_level, 0.0),
        "month": float(month),
    }


def predict_delay(
    model: SimpleRandomForest,
    route_distance: float,
    historical_delivery_time: float,
    weather: WeatherRead,
    month: int,
) -> tuple[bool, int]:
    features = _features_from_inputs(route_distance, historical_delivery_time, weather, month)
    missing = [feature for feature in FEATURES if feature not in features]
    if missing:
        raise ValueError(f"Missing features for prediction: {missing}")
    return model.predict_delay(features)


def get_model_with_fallback(data_path: str) -> SimpleRandomForest:
    try:
        return load_or_train_model(data_path)
    except FileNotFoundError:
        return load_or_train_model(data_path)
