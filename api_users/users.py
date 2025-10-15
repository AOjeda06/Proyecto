from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

UserList = [
    User(id=1, name="John", surname="Doe", age=30),
    User(id=2, name="Jane", surname="Smith", age=25),
    User(id=3, name="Alice", surname="Johnson", age=28)
]
@app.get("/users")
def users():
    return UserList

@app.get("/users/{id}")
def user(id: int):
    users = [user for user in UserList if user.id == id]
    if users:
        return users[0]
    return {"error": "User not found"}