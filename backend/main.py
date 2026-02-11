from typing import Union
from app.create_user import CreateUser, CreateUserHandler
from domain.exceptions import UsernameAlreadyExists
from domain.exceptions import EmailAlreadyExists
from domain.exceptions import DNIAlreadyExists
from infra import MemoryUsersRepo
from app import GetUsers, GetUsersHandler
from domain import User
from infra import QueryBus
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from infra.buses import CommandBus
from fastapi import HTTPException

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
q_bus.subscribe(GetUsers, h)

c_bus = CommandBus()
command_h = CreateUserHandler(repo_user)
c_bus.subscribe(CreateUser, command_h)
    
@app.get("/query/{q_name}")
def read_root(q_name):
    try:
        return [e.to_primitive() for e in q_bus.dispatch(q_name)]
    except:
        import traceback; traceback.print_exc()


@app.post("/command/{c_name}")
async def write_root(c_name: str, request: Request):
    
    try:
        c_info = await request.json()
        c_bus.dispatch(c_name,c_info)
    except UsernameAlreadyExists:
        raise HTTPException(status_code=400, detail="Username already exists")
    except EmailAlreadyExists:
        raise HTTPException(status_code=400, detail="Email already exists")
    except DNIAlreadyExists:
        raise HTTPException(status_code=400, detail="DNI already exists")
        


