from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError, PyJWTError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta, timezone

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    # password: 12345 
    "johndoe2": {
        "username": "johndoe2",
        "email": "johndoe2@gmail.com",
        "full_name": "John Doe 2",
        "disabled": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$uYNv8kxz7retOJ5oQo02wQ$ZepYH255L0y8ikmIjKfqUEPBL6haZHoSYU9T1pONO+c"
    }
}

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 10

SECRET_KEY = "1aff6790e2c656dac3c4b9240cfa6a7e221235725d73d005ba93102fc2ee3cd4"

password_hash = PasswordHash.recommended()

@router.post("/register", status_code=201)
def register(user: UserDB):
    if user.username not in users_db:
        hashed_password = password_hash.hash(user.password)
        user.password = hashed_password
        users_db[user.username] = user.model_dump()
        return user
    else:
        raise HTTPException(status_code=409, detail="User already exists")
    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form_data.username)
    if not user_db:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    user = UserDB(**users_db[form_data.username])
    if not password_hash.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = {"sub": user.username, "exp": expire}
    token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

async def authentication(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = User(**users_db[username])
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

@router.get("/auth/me")
async def me(user: User = Depends(authentication)):
    return user