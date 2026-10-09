
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.models import User, Chat, Message
from app.auth import get_user_id_from_token

router = APIRouter(prefix="/chats", tags=["Chat History"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        user_id = get_user_id_from_token(token)
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid login token.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user


class ChatCreate(BaseModel):
    title: str = Field(default="New Chat", max_length=255)


class MessageCreate(BaseModel):
    role: str
    content: str


def chat_to_dict(chat):
    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat(),
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at.isoformat(),
            }
            for message in sorted(chat.messages, key=lambda m: m.created_at)
        ],
    }


@router.get("")
def list_chats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chats = (
        db.query(Chat)
        .filter(Chat.user_id == user.id)
        .order_by(Chat.created_at.desc())
        .all()
    )
    return [chat_to_dict(chat) for chat in chats]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_chat(
    data: ChatCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = Chat(title=data.title, user_id=user.id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat_to_dict(chat)


@router.get("/{chat_id}")
def get_chat(
    chat_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id, Chat.user_id == user.id)
        .first()
    )
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")
    return chat_to_dict(chat)


@router.post("/{chat_id}/messages", status_code=status.HTTP_201_CREATED)
def save_message(
    chat_id: int,
    data: MessageCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.role not in ("user", "assistant"):
        raise HTTPException(status_code=400, detail="Invalid message role.")

    chat = (
        db.query(Chat)
        .filter(Chat.id == chat_id, Chat.user_id == user.id)
        .first()
    )
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found.")

    message = Message(
        chat_id=chat.id,
        role=data.role,
        content=data.content,
    )
    db.add(message)

    if data.role == "user" and chat.title == "New Chat":
        chat.title = data.content[:42]

    db.commit()
    db.refresh(message)

    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "created_at": message.created_at.isoformat(),
    }