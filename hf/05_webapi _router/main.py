from fastapi import FastAPI
from routers.items import router as items_router
from routers.login import router as login_router # 라우트 추가마다 이부분 수정 및 추가 (1)
from routers.file_upload import router as file_upload_router

app = FastAPI()
app.include_router(items_router)
app.include_router(login_router) # 라우트 추가마다 이부분을 수정 및 추가 (2)
app.include_router(file_upload_router)

# uvicorn main:app --reload
# get/items/
# get/items/1
# get/items/5
# post/auth/login/