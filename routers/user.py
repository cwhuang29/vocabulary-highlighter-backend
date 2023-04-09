from fastapi import Depends, APIRouter, WebSocket
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.user import getUserSetting, getDisplayUserByTokenData, updateUserCollectedWordsWS, updateUserSetting, updateUserSettingWS
from routers.dependency import tokenDataDep, dbUserDep
from structs.schemas.setting import Setting, UpdateSettingOut
from utils.enum import RouterGroupType

router = APIRouter(prefix='/users', tags=[RouterGroupType.USER])


@router.get('/me')
async def me(tokenData: tokenDataDep, db: Session = Depends(getDB)):
    resp = await getDisplayUserByTokenData(tokenData, db)
    return resp


@router.get('/setting', response_model=Setting)
async def getSetting(dbUser: dbUserDep, db: Session = Depends(getDB)) -> Setting:
    resp = await getUserSetting(dbUser, db)
    return resp


@router.put('/setting')
async def updateSetting(setting: Setting, dbUser: dbUserDep, db: Session = Depends(getDB)) -> UpdateSettingOut:
    # Note that the datetime object had been transformed to UTC timezone by fastapi already!!!
    resp = await updateUserSetting(dbUser, setting, db)
    return resp


@router.websocket('/setting')
async def updateSettingWebSocket(websocket: WebSocket, db: Session = Depends(getDB)) -> None:
    await updateUserSettingWS(websocket, db)


@router.websocket('/setting/collected-words')
async def updateCollectedWordsWebSocket(websocket: WebSocket, db: Session = Depends(getDB)) -> None:
    await updateUserCollectedWordsWS(websocket, db)
