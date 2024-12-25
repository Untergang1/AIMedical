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


# username, avatar, real_name, id, age, sex, height, weight

class UserOutput(BaseModel):
    username: str
    avatar: str
    age: int
    sex: str
    height: str
    weight: str
    addition: str


class UserOutRes(BaseModel):
    code: int
    data: UserOutput


class UserInfoInput(BaseModel):
    username: str
    age: int
    sex: str
    height: str
    weight: str
    addition: str


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


class CodeRes(BaseModel):
    code: int
