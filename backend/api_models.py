from typing import Optional, List, Dict, Literal
from enum import Enum

from pydantic import BaseModel


class Query(BaseModel):
    query: str


class CommonRes(BaseModel):
    code: int
    response: str


class Token(BaseModel):
    token: str


class TokenRes(BaseModel):
    code: int
    data: Token


class LoginMessage(BaseModel):
    username: str
    password: str


class Sex(str, Enum):
    male = "male"
    female = "female"


class UserInput(BaseModel):
    username: str
    password: str
    sex: Sex
    age: int
    height: float   # m
    weight: float   # kg
    avatar: str
    rname: str
    id: str


class UserOutput(BaseModel):
    roles: List[str]
    introduction: str
    avatar: str
    username: str
    real_name: str
    id: str


class UserOutRes(BaseModel):
    code: int
    data: UserOutput


class MedicalRecordsRes(BaseModel):
    code: int
    data: List[Dict[Literal['time', 'query', 'response'], str]]


class ChatInput(BaseModel):
    src: str
    messages: List
    username: str


class ChatRes(BaseModel):
    code: int
    text: str


class ErrorRes(BaseModel):
    code: int
    message: str
