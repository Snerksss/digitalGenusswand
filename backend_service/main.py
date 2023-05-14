from datetime import timedelta, datetime

import uvicorn as uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from data.persistence_manager import PersistenceManager

from backend_service.dependencies.authentification import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token
from backend_service.dependencies.persistence_manager import get_persistence_manager
from backend_service.routers import genusswand, user
from backend_service.schemas.authentification import Token


def run():
    app = FastAPI()


    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                     pm: PersistenceManager = Depends(get_persistence_manager)):
        user = authenticate_user(form_data.username, form_data.password, pm)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


    for router in [genusswand.router, user.router]:
        app.include_router(router)

    app.mount("/", StaticFiles(directory="./static", html=True), name="static")

    uvicorn.run(app, host="0.0.0.0", port=8000)
