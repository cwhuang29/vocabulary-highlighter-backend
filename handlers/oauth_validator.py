from datetime import datetime

from config import AZURE_LOGIN_CLIENT_ID, GOOGLE_LOGIN_IOS_CLIENT_ID
from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from utils.constant import OAUTH_AZURE_ISS, OAUTH_AZURE_VER, OAUTH_GOOGLE_ISS
from utils.enum import LoginMethodType
from utils.message import ERROR_MSG
from utils.type import OAuthTokenType


def verifyOAuthGoogleToken(oauthToken: GoogleOAuthToken):
    err = ValueError(ERROR_MSG.OAUTH_TOKEN_INVALID)
    if oauthToken.aud != GOOGLE_LOGIN_IOS_CLIENT_ID:
        raise err
    if oauthToken.iss not in OAUTH_GOOGLE_ISS:
        raise err
    if not oauthToken.sub:
        raise err
    # No need to verify exp here since we have passed it to google oauth verification api
    # if oauthToken.exp < datetime.now().timestamp():  # Not utcnow()
    #     raise err


def verifyOAuthAzureToken(oauthToken: AzureOAuthToken):
    err = ValueError(ERROR_MSG.OAUTH_TOKEN_INVALID)
    if oauthToken.aud != AZURE_LOGIN_CLIENT_ID:
        raise err
    if not oauthToken.iss.startswith(OAUTH_AZURE_ISS):
        raise err
    if oauthToken.ver != OAUTH_AZURE_VER:
        raise err
    if not oauthToken.oid:
        raise err
    if oauthToken.exp < datetime.now().timestamp():  # Not utcnow()
        raise err


def verifyOAuthToken(loginMethod: LoginMethodType, oauthToken: OAuthTokenType):
    if loginMethod == LoginMethodType.GOOGLE:
        verifyOAuthGoogleToken(oauthToken)
    if loginMethod == LoginMethodType.AZURE:
        verifyOAuthAzureToken(oauthToken)
