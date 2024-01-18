from typing import Optional

from fastapi import APIRouter
from fastapi.security import HTTPBearer
from quest_maker_api_shared_library.token_manager import TokenManager

from core.config.env import Env
from core.models.authentication import Credentials, Token
from core.services.authentication import AuthenticationService

token = APIRouter()
bearer = HTTPBearer()
service = AuthenticationService()
env = Env()
token_manager = TokenManager(key=env.JWT_SECRET_KEY.get_secret_value(),
                             jwt_expiration_time_in_minutes=env.JWT_EXPIRATION_TIME_IN_MINUTES,)


@token.post('/')
def generate(credentials: Credentials) -> Optional[Token]:
    try:
        is_match, auth_data = service.verify(credentials=credentials)
        if is_match:
            token = token_manager.encode_token(identifier=str(auth_data.id), scope='access_token')
            # token = token_manager.encode_token(identifier=str(auth_data.id))
            return Token(token=token)
    except Exception as e:
        raise e

