from typing import Optional, List, Dict, Literal
from enum import Enum

from pydantic import BaseModel


class CommonRes(BaseModel):
    code: int
    response: str


class LogoutRes(BaseModel):
    code: int
    data: str


class Token(BaseModel):
    token: str


class TokenRes(BaseModel):
    code: int
    data: Token


class LoginMessage(BaseModel):
    username: str
    password: str


class Sex(str, Enum):
    male = "男"
    female = "女"


class RegisterInput(BaseModel):
    username: str
    password: str


# username, avatar, real_name, id, age, sex, height, weight

class UserInfoOutput(BaseModel):
    username: str
    avatar: Optional[str] = "https://t8.baidu.com/it/u=2209273868,3140520502&fm=193"
    age: Optional[int] = None
    sex: Optional[Sex] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    addition: Optional[str] = None


class UserInfoOutRes(BaseModel):
    code: int
    data: UserInfoOutput


class UserInfoInput(BaseModel):
    username: str
    age: int
    sex: Sex
    height: str
    weight: str
    addition: Optional[str] = None


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
