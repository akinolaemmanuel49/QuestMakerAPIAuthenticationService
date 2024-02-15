from http import HTTPStatus
from typing import Optional

import requests
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from quest_maker_api_shared_library.token_manager import TokenManager
from quest_maker_api_shared_library.custom_types import PydanticObjectId

from core.config.env import Env
from core.models.authentication import AuthChangePassword, AuthCreate, AuthResponse, AuthUpdate
from core.services.authentication import AuthenticationService


auth = APIRouter()
bearer = HTTPBearer()
service = AuthenticationService()
env = Env()
token_manager = TokenManager(key=env.JWT_SECRET_KEY.get_secret_value(),
                             jwt_expiration_time_in_minutes=env.JWT_EXPIRATION_TIME_IN_MINUTES,)


@auth.post('/', status_code=HTTPStatus.CREATED)
# Create new authentication instance
def create_auth(data: AuthCreate) -> Optional[AuthResponse]:
    try:
        user = service.create(data=data)
        try:
            token = token_manager.encode_token(
                identifier=str(user.id))
            # Convert user profile data into a dict
            json_data = user.model_dump(
                exclude={'id', 'createdAt', 'updatedAt'})
            # Add new key 'auth_id'
            json_data['auth_id'] = str(user.id)
            if json_data.get('roles'):
                for role in json_data['roles']:
                    role['_id'] = str(role['_id'])
                    role['organizationId'] = str(role['organizationId'])
            if json_data.get('organizations'):
                for organization in json_data['organizations']:
                    organization['id'] = str(organization['id'])
                    organization['ownerId'] = str(organization['ownerId'])

            # Set up request headers
            headers = {'Authorization': f'Bearer {token}'}

            # Pass user profile details to users service to create
            # a new user in the user collection
            response = requests.post(url=f'{env.USER_SERVICE_URL}users/',
                                     json=json_data,
                                     headers=headers)

            if response.status_code == HTTPStatus.CREATED:
                return user
            else:
                raise HTTPException(status_code=response.status_code,
                                    detail='Failed to create a user in the User service')
        except Exception as e:
            service.delete(auth_id=str(user.id))
            raise e
    except Exception as e:
        raise e


@auth.get('/')
def read_auth(token: HTTPAuthorizationCredentials = Security(bearer)):
    payload = token_manager.decode_token(token=token.credentials)
    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        auth_id = str(payload['sub'])
        return service.read(auth_id=auth_id)
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


@auth.put('/')
def update_auth(data: AuthUpdate, token: HTTPAuthorizationCredentials = Security(bearer)):
    payload = token_manager.decode_token(token=token.credentials)
    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        auth_id = str(payload['sub'])
        backup = service.read(auth_id=auth_id)
        if backup:
            try:
                service.update(auth_id, data)

                # Convert user profile data into a dict
                json_data = data.model_dump(exclude_unset=True)

                json_data['auth_id'] = str(auth_id)
                if json_data.get('roles'):
                    for role in json_data['roles']:
                        role['_id'] = str(role['_id'])
                        role['organizationId'] = str(role['organizationId'])
                if json_data.get('organizations'):
                    for organization in json_data['organizations']:
                        organization['id'] = str(organization['id'])
                        organization['ownerId'] = str(organization['ownerId'])
                

                # Set up request headers
                headers = {'Authorization': f'Bearer {token.credentials}'}

                # Pass user profile details to users service to update
                # a user in the user collection
                response = requests.put(url=f'{env.USER_SERVICE_URL}users/',
                                        json=json_data,
                                        headers=headers)

                if response.status_code == HTTPStatus.OK:
                    return 'Successfully updated'
                else:
                    raise HTTPException(status_code=response.status_code,
                                        detail='Failed to update user in the User service')
            except Exception as e:
                service.update(auth_id=auth_id, data=backup.model_dump(
                    exclude={'id', 'createdAt', 'updatedAt', 'userType'}))
                raise e
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


@auth.delete('/deactivate/', status_code=HTTPStatus.NO_CONTENT)
def deactivate_account(token: HTTPAuthorizationCredentials = Security(bearer)):
    payload = token_manager.decode_token(token=token.credentials)
    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        auth_id = str(payload['sub'])
        service.delete(auth_id=auth_id)
        return 'Successfully deleted'
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


@auth.put('/change-password/')
def change_password(data: AuthChangePassword, token: HTTPAuthorizationCredentials = Security(bearer)):
    from core.utils.hash_manager import HashManager

    hash_manager = HashManager()

    payload = token_manager.decode_token(token=token.credentials)
    scope = str(payload['scope'])
    if 'access_token' in scope.split():
        auth_id = payload['sub']
        data = {'passwordHash': hash_manager.hash_password(
            password=data.password)}
        service.update(auth_id, data=data)
        return 'Successfully changed password'
    else:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail={
                            'message': 'Insufficient scope'})


# @auth.get('/{auth_id}/')
# def debug_read(auth_id: PydanticObjectId):
#     return service.read(auth_id=str(auth_id))
