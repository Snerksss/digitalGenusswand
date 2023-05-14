import json

from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse
from data.persistence_manager import PersistenceManager

from data.model.user import User
from data.model.strich import Strich
from data.model.genusswand import Genusswand
from typing import List
from backend_service.dependencies.authentification import get_current_user
from backend_service.dependencies.persistence_manager import get_persistence_manager
import uuid
import time
from datetime import datetime

router = APIRouter(
    prefix="/genusswand",
    tags=["genusswand"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def get_genusswaende_for_specific_user(genusswaende: list, user: User):
    user_genusswaende = []
    for genusswand in genusswaende:
        if genusswand.user == user:
            user_genusswaende.append(genusswand)
    return user_genusswaende


def get_json_genusswaende(genusswaende: list):
    genusswaende_json = []
    for genusswand in genusswaende:
        genusswand_json = {"uuid": genusswand.uuid,
                           "name": genusswand.name}
        genusswaende_json.append(genusswand_json)
    return genusswaende_json


def get_json_genusswand_v2(genusswand: Genusswand):
    striche = []
    for strich in genusswand.striche:
        strich_json = {"uuid": strich.uuid,
                       "mistaker": strich.mistaker,
                       "reason": strich.reason,
                       "reporter": strich.reporter,
                       "timestamp": datetime.utcfromtimestamp(strich.timestamp).strftime('%Y-%m-%d')
                       }
        striche.append(strich_json)
    genusswand_json = {"uuid": genusswand.uuid,
                       "owner": genusswand.user_username,
                       "striche": striche}
    return genusswand_json


def sortMistakers(mistakers: [], mistakers_names: []):
    sorted_mistakers_json = []
    mistakers_names.sort()
    for mistaker_name in mistakers_names:
        for mistaker in mistakers:
            if mistaker_name == mistaker['mistaker']:
                sorted_mistakers_json.append(mistaker)
                break
    return sorted_mistakers_json


def get_json_genusswand_v1(genusswand: Genusswand):
    mistakers_json = []
    mistakers_name = []
    for strich in genusswand.striche:
        newMistaker = True
        for mistaker in mistakers_json:
            if mistaker['mistaker'] == strich.mistaker:
                mistaker['counter'] = mistaker['counter'] + 1
                newMistaker = False
        if newMistaker:
            x = {"mistaker": strich.mistaker,
                 "counter": 1}
            mistakers_name.append(strich.mistaker)
            mistakers_json.append(x)
    genusswand_json = {"mistakers": sortMistakers(mistakers_json, mistakers_name)}
    return genusswand_json


@router.post("/create/genusswand")
async def create_genusswand(name: str = Body(embed=True),
                            pm: PersistenceManager = Depends(get_persistence_manager),
                            auth_user: User = Depends(get_current_user)):
    if auth_user is None or name is None or name == '':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    else:
        new_genusswand = Genusswand()
        new_genusswand.uuid = str(uuid.uuid4())
        new_genusswand.user_username = auth_user.username
        new_genusswand.name = name
        pm.save_object(new_genusswand)
        return JSONResponse(status_code=status.HTTP_200_OK, content="Genusswand created")


@router.post("/create/strich_v1")
async def create_strich_v1(mistaker: str = Body(embed=True),
                           uuid_genusswand: str = Body(embed=True),
                           pm: PersistenceManager = Depends(get_persistence_manager),
                           auth_user: User = Depends(get_current_user)):
    if auth_user is None or mistaker is None or mistaker == '' or uuid_genusswand is None or uuid_genusswand == '':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    else:
        genusswand: Genusswand = pm.get_object(Genusswand, uuid_genusswand)
        if genusswand is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Genusswand doesn't exists")
        else:
            new_strich = Strich()
            new_strich.uuid = str(uuid.uuid4())
            new_strich.timestamp = time.time()
            new_strich.mistaker = mistaker
            new_strich.reporter = ""
            new_strich.reason = "unknown"
            new_strich.genusswand_uuid = genusswand.uuid
            pm.save_object(new_strich)
            return JSONResponse(status_code=status.HTTP_200_OK, content="Strich created")


@router.post("/create/strich_v2")
async def create_strich_v2(mistaker: str = Body(embed=True),
                           reporter: str = Body(embed=True),
                           reason: str = Body(embed=True),
                           uuid_genusswand: str = Body(embed=True),
                           pm: PersistenceManager = Depends(get_persistence_manager),
                           auth_user: User = Depends(get_current_user)):
    if auth_user is None or mistaker is None or mistaker == '' or reporter is None or reporter == '' or reason is None \
            or reason == '' or uuid_genusswand is None or uuid_genusswand == '':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    else:
        genusswand: Genusswand = pm.get_object(Genusswand, uuid_genusswand)
        if genusswand is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Genusswand doesn't exists")
        else:
            new_strich = Strich()
            new_strich.uuid = str(uuid.uuid4())
            new_strich.timestamp = time.time()
            new_strich.mistaker = mistaker
            new_strich.reporter = reporter
            new_strich.reason = reason
            new_strich.genusswand_uuid = genusswand.uuid
            pm.save_object(new_strich)
            return JSONResponse(status_code=status.HTTP_200_OK, content="Strich created")


@router.delete("/delete/strich_v1")
async def delete_strich_v1(mistaker: str = Body(embed=True),
                           uuid_genusswand: str = Body(embed=True),
                           pm: PersistenceManager = Depends(get_persistence_manager),
                           auth_user: User = Depends(get_current_user)):
    if auth_user is None or mistaker is None or mistaker == '' or uuid_genusswand is None or uuid_genusswand == '':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    else:
        genusswand: Genusswand = pm.get_object(Genusswand, uuid_genusswand)
        if genusswand is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Genusswand doesn't exists")
        else:
            striche: List[Strich] = genusswand.striche
            for strich in striche:
                if strich.mistaker == mistaker:
                    pm.delete_object(strich)
                    return JSONResponse(status_code=status.HTTP_200_OK, content="Strich deleted")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Mistaker doesn't exists")


@router.get("/get/genusswaende")
async def get_genusswaende(pm: PersistenceManager = Depends(get_persistence_manager),
                           auth_user: User = Depends(get_current_user)):
    if auth_user is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    else:
        user_genusswaende = get_genusswaende_for_specific_user(pm.get_objects(Genusswand), auth_user)
        return JSONResponse(status_code=status.HTTP_200_OK, content=get_json_genusswaende(user_genusswaende))


@router.get("/get/genusswand/{uuid}")
async def get_genusswand_data(uuid: str,
                              pm: PersistenceManager = Depends(get_persistence_manager),
                              auth_user: User = Depends(get_current_user)):
    if auth_user is None or uuid == '':
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Wrong Input")
    else:
        genusswand: Genusswand = pm.get_object(Genusswand, uuid)
        if genusswand is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Genusswand doesn't exists")
        else:
            if genusswand.user == auth_user:
                return JSONResponse(status_code=status.HTTP_200_OK, content=get_json_genusswand_v1(genusswand))
            else:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content="Genusswand isn't belonging to you")
