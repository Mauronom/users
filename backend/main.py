from typing import Union
from infra import MemoryUsersRepo
from app import GetUsers, GetUsersHandler
from domain import User
from infra import QueryBus
import json
from fastapi import FastAPI

app = FastAPI()

q_bus = QueryBus()
u = User('1', 'u1', 'u1@test.com', '12345678A')
repo_user = MemoryUsersRepo([u])
h = GetUsersHandler(repo_user)
q = GetUsers()
q_bus.subscribe(GetUsers, h)
    
@app.get("/query/{q_name}")
def read_root(q_name):
    return [str(e) for e in q_bus.dispatch(q_name)]

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
