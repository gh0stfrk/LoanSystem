from app.models import User
from app.schemas import CreateUser
from sqlalchemy.orm import Session
from app.utils import create_hash, validate_hash


def get_user(user_id:int, db: Session)-> User:
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    return user


def create_user(user: CreateUser, db: Session) -> User:
    new_user = User(
        email = user.email,
        hashed_password = create_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    
    return new_user

