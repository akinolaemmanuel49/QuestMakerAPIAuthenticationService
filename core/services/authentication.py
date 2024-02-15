from datetime import datetime
from typing import Any, Dict, Optional, Union

from bson import ObjectId
from pymongo.errors import DuplicateKeyError as MongoDBDuplicateKeyError
from quest_maker_api_shared_library.custom_types import PydanticObjectId
from quest_maker_api_shared_library.errors.database import DuplicateKeyError

from core.models.authentication import AuthCreate, AuthInDB, AuthOutDB, AuthResponse, AuthUpdate, Credentials
from core.utils.hash_manager import HashManager
from core.config.env import Env
from core.config.database import AuthDatabase

env = Env()
hash_manager = HashManager()
db = AuthDatabase()


class AuthenticationService:
    def create(self, data: AuthCreate) -> AuthResponse:
        try:
            # Load data into AuthInDB container
            auth = AuthInDB(
                email=data.email,
                # Hash the password and store it in the passwordHash field
                passwordHash=hash_manager.hash_password(data.password),
                firstName=data.firstName,
                lastName=data.lastName,
                roles=data.roles,
                organizations=data.organizations,
                userType=data.userType,
                createdAt=str(datetime.utcnow()),
                updatedAt=str(datetime.utcnow())
            )

            # Convert the AuthInDB container into a dict
            auth_dict = auth.model_dump()

            # Create new auth instance in database collection
            document = db.auth_collection.insert_one(auth_dict)

            # Load auth_dict into AuthResponse container
            response = AuthResponse(
                _id=str(document.inserted_id),
                email=auth.email,
                firstName=auth.firstName,
                lastName=auth.lastName,
                roles=auth.roles,
                organizations=auth.organizations,
                userType=auth.userType,
                createdAt=auth.createdAt,
                updatedAt=auth.updatedAt
            )

            # Return the AuthResponse container
            return response

        except MongoDBDuplicateKeyError:
            raise DuplicateKeyError

        except Exception as e:
            raise e

    def read(self, auth_id: PydanticObjectId) -> Optional[AuthResponse]:
        try:
            document = db.auth_collection.find_one({'_id': ObjectId(auth_id)})
            if document:
                if document['organizations']:
                    for organization in document['organizations']:
                        organization['id'] = str(organization['id'])
                        organization['ownerId'] = str(organization['ownerId'])
                if document['roles']:
                    for role in document['roles']:
                        role['_id'] = str(role['_id'])
                        role['organizationId'] = str(role['organizationId'])
                document = AuthResponse(**document)
                return document
            return None
        except Exception as e:
            raise e

    # def update(self, auth_id: PydanticObjectId, data: Union[AuthUpdate, AuthChangePassword]):
    def update(self, auth_id: PydanticObjectId, data: Union[AuthUpdate, Dict[str, Any]]):
        try:
            if isinstance(data, AuthUpdate):
                data = data.model_dump(exclude_unset=True)

            # Update and convert date in updatedAt field to string
            data['updatedAt'] = str(datetime.utcnow())
            if data.get('organizations'):
                for organization in data['organizations']:
                    organization['id'] = ObjectId(organization['id'])
                    organization['ownerId'] = ObjectId(organization['ownerId'])
            if data.get('roles'):
                for role in data['roles']:
                    role['_id'] = ObjectId(role['_id'])
                    role['organizationId'] = ObjectId(role['organizationId'])

            db.auth_collection.update_one(
                {'_id': ObjectId(auth_id)}, {'$set': data})
        except Exception as e:
            raise e

    def delete(self, auth_id: PydanticObjectId):
        try:
            # Delete an auth instance using it's id
            db.auth_collection.delete_one({'_id': ObjectId(auth_id)})
        except Exception as e:
            raise e

    def verify(self, credentials: Credentials):
        try:
            # Retrieve an auth instance using the associated email address
            document = db.auth_collection.find_one(
                {'email': credentials.email})
            if document:
                out = AuthOutDB(**document)
                is_match = hash_manager.verify_password(
                    credentials.password.get_secret_value(), out.passwordHash
                )
                if is_match:
                    return is_match, out
                else:
                    raise ValueError('Invalid password')
        except Exception as e:
            raise e
