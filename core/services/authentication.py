from datetime import datetime
from typing import Any, Dict, Union

from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from quest_maker_api_shared_library.custom_types import PydanticObjectId

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
                roleIds=data.roleIds,
                organizationId=data.organizationId,
                userType=data.userType,
                createdAt=str(datetime.utcnow()),
                updatedAt=str(datetime.utcnow())
            )

            # Convert the AuthInDB container into a dict
            auth_dict = auth.model_dump()

            # Create new auth instance in database collection
            document = db.auth_collection.insert_one(auth_dict)

            # Load auth_dict int AuthResponse container
            user = AuthResponse(
                _id=str(document.inserted_id),
                email=auth.email,
                firstName=auth.firstName,
                lastName=auth.lastName,
                roleIds=auth.roleIds,
                organizationId=auth.organizationId,
                userType=auth.userType,
                createdAt=auth.createdAt,
                updatedAt=auth.updatedAt
            )

            # Return the AuthResponse container
            return user

        except DuplicateKeyError:
            raise ValueError(
                "Auth credentials with the same email already exist")

        except Exception as e:
            raise e

    def read(self, auth_id: PydanticObjectId) -> AuthResponse:
        try:
            document = db.auth_collection.find_one({'_id': ObjectId(auth_id)})
            # Convert ObjectId to string
            document['_id'] = str(document['_id'])
            document = AuthResponse(**document)
            return document
        except Exception as e:
            raise e

    # def update(self, auth_id: PydanticObjectId, data: Union[AuthUpdate, AuthChangePassword]):
    def update(self, auth_id: PydanticObjectId, data: Union[AuthUpdate, Dict[str, Any]]):
        try:
            if isinstance(data, AuthUpdate):
                data = data.model_dump(exclude_unset=True)
            # Update and convert date in updatedAt field to string
            data['updatedAt'] = str(datetime.utcnow())
            # Find and update an auth instance
            db.auth_collection.update_one(
                {'_id': ObjectId(auth_id)}, {'$set': data})
        except Exception:
            pass

    def delete(self, auth_id: PydanticObjectId):
        try:
            # Delete an auth instance using it's id
            db.auth_collection.delete_one({"_id": ObjectId(auth_id)})
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
