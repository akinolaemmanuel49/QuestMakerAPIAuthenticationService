from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, SecretStr
from quest_maker_api_shared_library.custom_types import PydanticObjectId


class Organization(BaseModel):
    id: PydanticObjectId = Field(alias='id')
    name: str
    description: Optional[str]
    ownerId: PydanticObjectId = Field(alias='ownerId')
    createdAt: str
    updatedAt: str


class AuthCreate(BaseModel):
    email: str
    password: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []
    userType: str = 'regular'


class AuthUpdate(BaseModel):
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Any = []
    organizations: Optional[List[Organization]] = []


class AuthResponse(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []
    userType: str
    createdAt: str
    updatedAt: str


class AuthInDB(BaseModel):
    email: str
    passwordHash: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    roles: Optional[List[Dict[str, Any]]] = []
    organizations: Optional[List[Organization]] = []
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


class Message(BaseModel):
    statusCode: int
    message: str
    data: Any


class ErrorMessage(Message):
    pass
