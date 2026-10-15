from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

# --- SCHEMAS PARA USUÁRIO ---

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- SCHEMAS PARA MENSAGENS ---

class MessageCreate(BaseModel):
    sender_id: int
    recipient_id: int
    body: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    body: str
    sent_at: datetime

    model_config = ConfigDict(from_attributes=True)

