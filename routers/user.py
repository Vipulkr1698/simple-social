from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import func

# from sqlalchemy.sql.functions import func
from database import get_db
import schemas, models
from utils import get_password_hash

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hash_pwd = get_password_hash(user.password)
    user.password = hash_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=List[schemas.UserOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
