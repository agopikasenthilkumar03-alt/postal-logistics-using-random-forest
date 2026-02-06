from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import ROLE_ADMIN, ROLE_CUSTOMER, ROLE_STAFF, require_role
from app.db.session import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostRead, dependencies=[Depends(require_role({ROLE_STAFF, ROLE_ADMIN}))])
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    if db.query(Post).filter(Post.post_id == payload.post_id).first():
        raise HTTPException(status_code=409, detail="Post ID already exists")
    post = Post(**payload.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("", response_model=list[PostRead], dependencies=[Depends(require_role({ROLE_ADMIN, ROLE_STAFF}))])
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@router.get("/{post_id}", response_model=PostRead, dependencies=[Depends(require_role({ROLE_CUSTOMER, ROLE_ADMIN, ROLE_STAFF}))])
def get_post(post_id: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
