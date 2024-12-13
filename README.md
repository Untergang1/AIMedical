## TODO List

### 修复对话框

### 添加科室选项 

儿科，内科，外科，眼科，牙科，皮肤科

### 添加个人信息选项

包括性别，年龄，身高，体重以及病历。

### 查看病历

后端接口：

```
@app.get("/user/info/medical_records", response_model=MedicalRecordsRes | ErrorRes, status_code=status.HTTP_200_OK)
async def get_medical_records(username: str):
...

class MedicalRecordsRes(BaseModel):
    code: int
    data: List[Dict[Literal['time', 'query', 'response'], str]]
    
class ErrorRes(BaseModel):
    code: int
    message: str
```

### 添加上传图片功能

后端接口：

```
@app.post("/user/chat", response_model=ChatRes)
async def get_model_response(
    src: str = Form(...),
    messages: List[str] = Form(...),
    image: UploadFile = File(None),
    username: str = Form(...),
):
...

class ChatRes(BaseModel):
    code: int
    text: str
    
class ErrorRes(BaseModel):
    code: int
    message: str
```