from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from schema import UserCreate, UserLogin, UserResponse
from DB.db import create_user, find_user_by_email, get_db, verify_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, name=user.name, email=user.email, password=user.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login/", response_model=UserResponse, status_code=200)
async def login_user_endpoint(user: UserLogin, db: Session = Depends(get_db)):
    try:
        user = verify_user(db, email=user.email, password=user.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/lookup/", response_model=UserResponse, status_code=200)
async def lookup_user_by_email_endpoint(email: EmailStr, db: Session = Depends(get_db)):
    try:
        user = find_user_by_email(db, email=email.strip())
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))