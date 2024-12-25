from fastapi import FastAPI, File, UploadFile, Form, Response, status
from model import GeminiModel
from fastapi.middleware.cors import CORSMiddleware
from tempfile import NamedTemporaryFile

from log import get_logger
from prompts import get_sys_prompt
from user_database import UserDatabase
from api_models import *
from utils import sex_e2z_dict

logger = get_logger(__name__)

app = FastAPI()

origins = [
    "*",
]

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = GeminiModel()
# model = None
user_db = UserDatabase()

# user_db.insert_user({'username': 'admin',
#                      'password': '123456',
#                      'roles': ['admin'],
#                      'introduction': "introduction",
#                      'avatar': "https://media1.tenor.com/m/VPW95GiH_BwAAAAC/blue-archive-ni-ga.gif",
#                      'real_name': "real name",
#                      'id': "3310022004040400030",
#                      'sex': '',
#                      'age': 25,
#                      'height': 1.72,    # m
#                      'weight': 72,      # kg
#                      'medical_records': []
#                      })


@app.post("/user/login", response_model=TokenRes | ErrorRes, status_code=status.HTTP_200_OK)
async def login(message: LoginMessage):
    success, mes = user_db.verify_usr(message.username, message.password)
    if success:
        logger.info(f"{message.username} log in.")
        token = Token(token=message.username)
        return TokenRes(code=20000, data=token)
    else:
        logger.error(f"log in failed, {message.username} {mes}.")
        return ErrorRes(code=40000, message=mes)


@app.get("/user/info", response_model=UserOutRes | ErrorRes, status_code=status.HTTP_200_OK)
async def query_user(token: str):
    result = user_db.query_name(token)
    result.pop("_id", None)
    logger.debug(f"res: {result}")
    result['height'] = str(result['height'])
    result['weight'] = str(result['weight'])
    user_out = UserOutput(**result)
    logger.info(f"response user info:{user_out.dict()}")
    if result:
        return UserOutRes(code=20000, data=result)
    else:
        return ErrorRes(code=40000, message="user not exist")


@app.post("/user/info", response_model=CodeRes | ErrorRes, status_code=status.HTTP_200_OK)
async def update_user(user_info: UserInfoInput):
    logger.debug("111111111111111111111111111111")
    result = user_db.update_user(user_info.dict())
    logger.info(f"user info update")
    if result:
        return CodeRes(code=20000)
    else:
        return ErrorRes(code=40000, message="user not exist")


@app.get("/user/info/medical_records", response_model=MedicalRecordsRes | ErrorRes, status_code=status.HTTP_200_OK)
async def get_medical_records(username: str):
    result = user_db.query_name(username)
    records = result['medical_records']
    logger.info(f"response user {username}'s medical records: {records}")
    if result:
        return MedicalRecordsRes(code=20000, data=records)
    else:
        return ErrorRes(code=40000, message="user not exist")


@app.post("/user/register", response_model=CommonRes | ErrorRes)
async def register(user_info: UserInput):
    user_info = user_info.dict()
    user_info['medical_records'] = []
    result = user_db.insert_user(user_info)
    if result:
        logger.info(f"{user_info['username']} registered")
        return CommonRes(code=20000, response=f"{user_info['username']} register successful")
    else:
        logger.error(f"register failed, {user_info['username']} existed")
        return ErrorRes(code=40000, message="username has existed.")


@app.post("/user/chat", response_model=ChatRes)
async def get_model_response(chat_input: ChatInput):
    image_paths = []
    src = chat_input.src
    username = chat_input.username
    query = chat_input.messages[-1]['text']
    history = chat_input.messages[:-1]

    logger.debug(f'src: {src}')
    logger.debug(f"history: {history}")
    logger.info(f"get query: {query}")

    rag_prompt = model.rag(query)
    sys_prompt = get_sys_prompt(src)

    user_info = user_db.query_name(username)
    user_sex = user_info['sex']
    user_age = user_info['age']
    user_height = user_info['height']
    user_weight = user_info['weight']
    user_info_prompt = f"性别：{user_sex}，年龄：{user_age}，身高：{user_height}，体重：{user_weight}\n"

    medical_record_prompt = ""
    medical_records = user_info['medical_records']
    if len(medical_records) == 0:
        medical_record_prompt = medical_record_prompt + "无\n"
    else:
        for record in medical_records:
            time = record['time']
            describe = record['query']
            medical_record_prompt = medical_record_prompt + time + ": " + describe + "\n"

    prompt = (sys_prompt
              + "\n你可以参考以下案例：\n" + rag_prompt
              + "患者病历：\n" + medical_record_prompt
              + "患者基本信息：\n" + user_info_prompt
              + "患者问题：\n" + query
              + "\n请用纯文本的方式输出，不要使用markdown格式"
              )

    logger.debug(f"prompt: {prompt}")
    response_text = model.get_response(query, images=image_paths, history=history)
    logger.info(f"send response: {response_text}")

    user_db.insert_medical_record(username, query, response_text)

    return ChatRes(code=20000, text=response_text)


# 处理用户输入并调用模型（支持可选的图片上传）
# @app.post("/user/chat", response_model=CommonResponse)
# async def get_model_response(
#     query: str = Form(...),
#     image: UploadFile = File(default=None)
# ):
#     image_paths = []
#     if image:
#         image_path = f"./uploaded_images/{image.filename}"
#         with open(image_path, "wb") as f:
#             f.write(await image.read())
#         image_paths.append(image_path)
#
#     logger.info(f"get query: {query}")
#     prompt = model.rag(query)
#     prompt = triage_prompt + prompt
#     logger.debug(f"prompt: {prompt}")
#     response_text = model.get_response(prompt, images=image_paths)
#     logger.info(f"send response: {response_text}")
#
#     return CommonResponse(response=response_text)
