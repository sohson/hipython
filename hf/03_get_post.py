from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
  return {'message':'Hello, FastAPI'}


@app.get("/hello") # get은 서버에 있는 데이터 조회 > URL
def say_hello():
  return{"message":"안녕하세요!"}

@app.post("/echo") # post는 서버에 새로운 데이터를 보내기 > HTTP Body 
def echo(data: dict):
  return {"dict":data}

@app.get("/test1")
def root1():
  return{"name":"둘리"}

@app.get("/test2")
def root2():
  return["둘리", "또치", "도우너"]

@app.get("/test3")
def root3():
  return "<h1>안녕?</h1>"

@app.get("/test4")
def root4():
  return 2000

def read_item(item_id:int):
  print(f'{item_id}를 받았습니다')
  return {"ID": item_id}

#경로매개변수, 핸들러
@app.get("/items/{item_id}")
def read_item(item_id: int, discount:bool=False):
  item_id = item_id*2
  return{'ID':item_id, 'discount':discount}

#쿼리 매개변수 > ? 뒤에 온다
# http://127.0.0.1:8000/items/3?discount=true

# http://127.0.0.1:8000/items/3/orders/2
@app.get("/items/{item_id}/orders/{order_id}")
def get_item_orders(item_id:int, order_id:int):
  return {"item_id":item_id, "order_id":order_id}

# http://127.0.0.1:8000/stocks/005930/history?days=60&market=kospi
@app.get("/stocks/{ticker}/history")
def get_stock_history(
  ticker:str, days:int, market:str
):
  print("get_stock_history > 종목 이력을 조회합니다.")
  return{"ticker":"", "days":60, "history":"구현예정입니다."}

from pydantic import BaseMode
class News(BaseModel):
  title: str
  content: str
  views: int=0

@app.post("/views")
