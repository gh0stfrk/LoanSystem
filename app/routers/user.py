from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import CreateUser
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.services.users import create_user

users = APIRouter(
    prefix="/user",
    tags = ['Registration']
)


@users.post("")
async def create_new_user(user: CreateUser, db=Depends(get_db)):
    try:
        user = create_user(user, db)
        return JSONResponse(
            {
                "user_id": user.id,
                "email": user.email
            },
            status_code=200
        )
    except IntegrityError:
        return HTTPException(
            detail={
                "msg":f"User with {user.email} exists"
            },
            status_code=400
        )
    except Exception as e:
        return HTTPException(detail={
            "status": "Failed",
            "message": f"{e}"
        }, status_code=400
        )
