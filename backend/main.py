from typing import Union
from infra import MemoryUsersRepo
from app import GetUsers, GetUsersHandler
from domain import User
from infra import QueryBus
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

q_bus = QueryBus()
u = User('1', 'u1', 'u1@test.com', '12345678A')
repo_user = MemoryUsersRepo([u])
h = GetUsersHandler(repo_user)
q = GetUsers()
q_bus.subscribe(GetUsers, h)
    
@app.get("/query/{q_name}")
def read_root(q_name):
    print('hoooooloaaaaa')
    try:
        print([str(e) for e in q_bus.dispatch(q_name)])
        return [{'a':3}]
        return [str(e) for e in q_bus.dispatch(q_name)]
    except:
        import traceback; traceback.print_exc()


