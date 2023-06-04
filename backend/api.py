from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List
from database import SessionLocal

# Database configuration
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# Models
class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String)
    address = Column(String)

# Pydantic models for request and response
class UserCreate(BaseModel):
    email: str
    password: str
    address: str

class UserResponse(BaseModel):
    id: int
    email: str
    address: str

# FastAPI app
app = FastAPI()

# Dependency to get database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# API endpoints
@app.get("/users/all", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    user_responses = [UserResponse(id=user.id, email=user.email, address=user.address) for user in users]
    return user_responses


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, password=user.password, address=user.address)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_response = UserResponse(
        id=db_user.id,
        email=db_user.email,
        address=db_user.address
    )
    return user_response


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_response = UserResponse(id=user.id, email=user.email, address=user.address)
    return user_response

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


