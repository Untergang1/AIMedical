from fastapi import FastAPI, Form, File, UploadFile
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/query")
async def process_query(
    query: str = Form(...),
    image: UploadFile = File(default=None)
):
    """
    接收文字字段和可选的图片
    - `query`: 必须的字符串字段
    - `image`: 可选的图片文件
    """
    response_data = {"query": query}
    print(query)

    if image:
        # 如果上传了图片，处理图片信息
        response_data["image_name"] = image.filename
        response_data["image_content_type"] = image.content_type
        # 如果需要保存文件，可以这样操作：
        with open(f"./uploaded_images/{image.filename}", "wb") as f:
            f.write(await image.read())
        print(image.filename)
        print(image.content_type)

    return JSONResponse(content=response_data)
