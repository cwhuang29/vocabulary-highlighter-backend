from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from handlers.auth import handleLogin, handleLogout
from routers.dependency import tokenDataDep, tryToGetTokenDataDep, sourceHeaderDep, deivcePlatformHeaderDep
from structs.requests.auth import ReqLogin
from databases.setup import getDB
from structs.schemas.auth import LoginOut
from utils.enum import RouterGroupType

router = APIRouter(tags=[RouterGroupType.AUTH])


@router.post('/login', response_model=LoginOut)
async def login(reqLogin: ReqLogin, tokenData: tryToGetTokenDataDep, source: sourceHeaderDep, platform: deivcePlatformHeaderDep, db: Session = Depends(getDB)):
    resp = await handleLogin(reqLogin, tokenData, source, platform, db)
    return resp


@router.post('/logout')
async def logout(tokenData: tokenDataDep, source: sourceHeaderDep, db: Session = Depends(getDB)):
    await handleLogout(tokenData, source, db)
    return {'result': 'success'}
