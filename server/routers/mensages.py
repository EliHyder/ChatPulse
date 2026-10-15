from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from DB.db import create_message, get_db, get_message_send_receive, get_messages_for_user
from schema import MessageCreate, MessageResponse

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
async def create_message_endpoint(message: MessageCreate, db: Session = Depends(get_db)):
    try:
        new_message = create_message(db, sender_id=message.sender_id, recipient_id=message.recipient_id, body=message.body)
        return new_message
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}/", response_model=dict, status_code=200)
async def get_messages_for_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    try:
        messages = get_messages_for_user(db, user_id=user_id)
        return messages
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversation/{sender_id}/{recipient_id}/", response_model=dict, status_code=200)
async def get_message_send_receive_endpoint(sender_id: int, recipient_id: int, db: Session = Depends(get_db)):
    try:
        messages = get_message_send_receive(db, sender_id=sender_id, recipient_id=recipient_id)
        return messages
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))