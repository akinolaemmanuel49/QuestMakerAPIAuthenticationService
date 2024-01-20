from typing import List, Optional
from pydantic import BaseModel, Field, SecretStr
from quest_maker_api_shared_library.custom_types import PydanticObjectId


class AuthCreate(BaseModel):
    email: str
    password: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []
    userType: str = 'regular'


class AuthUpdate(BaseModel):
    email: Optional[str] =  None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []


class AuthResponse(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []
    userType: str
    createdAt: str
    updatedAt: str


class AuthInDB(BaseModel):
    email: str
    passwordHash: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roleIds: Optional[List[PydanticObjectId]] = []
    organizationIds: Optional[List[PydanticObjectId]] = []
    userType: str
    createdAt: str
    updatedAt: str


class AuthOutDB(AuthInDB):
    id: PydanticObjectId = Field(alias='_id')


class Credentials(BaseModel):
    email: str
    password: SecretStr


class Token(BaseModel):
    token: str


class AuthChangePassword(BaseModel):
    password: str
