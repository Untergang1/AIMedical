from typing import Optional, List
from enum import Enum

from pydantic import BaseModel


class Query(BaseModel):
    query: str


class CommonResponse(BaseModel):
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


# user_db.insert_user({'username': 'admin',
#                      'password': '123456',
#                      'roles': ['admin'],
#                      'introduction': "introduction",
#                      'avatar': "https://media1.tenor.com/m/VPW95GiH_BwAAAAC/blue-archive-ni-ga.gif",
#                      'real_name': "real name",
#                      'id': "3310022004040400030",
#                      'sex': 'male',
#                      'age': 25,
#                      })


class UserInput(BaseModel):
    username: str
    password: str
    sex: Optional[Sex] = None
    age: Optional[int] = None
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


class ChatInput(BaseModel):
    src: str
    messages: List


class ChatRes(BaseModel):
    code: int
    text: str


class ErrorRes(BaseModel):
    code: int
    message: str
