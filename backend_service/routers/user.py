from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse, FileResponse
from data.persistence_manager import PersistenceManager

from data.model.user import User
from backend_service.dependencies.authentification import get_current_user, hash_password
from backend_service.dependencies.persistence_manager import get_persistence_manager

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


# erstellung von user account
@router.post("/create")
async def create(username: str = Body(embed=True),
                 passwd: str = Body(embed=True),
                 email: str = Body(embed=True),
                 pm: PersistenceManager = Depends(get_persistence_manager)):
    if username is None or username == '' or passwd is None or passwd == '' or email is None or email == '' \
            or pm.get_object(User, username) is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    user = User()
    user.first_name = "Unknown"
    user.last_name = "Unknown"
    user.username = username
    user.email = email
    user.passwd = hash_password(passwd)
    pm.save_object(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Neuer User erstellt")


# zurueckgabe von bestimmten User Informationen
@router.get("/me")
async def get(auth_user: User = Depends(get_current_user)):
    if auth_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="No User")
    return {"first_name": auth_user.first_name, "last_name": auth_user.last_name, "username": auth_user.username,
            "email": auth_user.email}
