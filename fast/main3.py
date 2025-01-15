from fastapi import FastAPI,Query,Path,Body,HTTPException, status
from  enum  import Enum
from pydantic import BaseModel,Field,HttpUrl,EmailStr
from typing import Annotated,Literal
from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import FastAPI, HTTPException,Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from sqlmodel import Field,Session,SQLModel,create_engine,select
import uuid
from  model import Hero, DatabaseRes
from databse import get_session, engine




app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Items(BaseModel):
    name: str
    description : str | None =Field(default=None, title='the description of the product', max_length=300)
    price: float = Field(ge=0, description='the price must be greater than zero')
    tax: float  | None=None
    tags: set[str] = set()
    image: list[Image] | None = None



class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Items]

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put('/update_product/{sales_id}')
async def update_product(sales_id:Annotated[int, Path(title='sales id', ge=0, le=100)], item: Items, q:str | None=None):
     result = {"item_id":sales_id }

     if q:
         result.update({'q':q})
     if item:
         result.update({
             'itmes': item
         })
     return result


@app.put("/user/{user_id}")
async def updated_user(user_id: int,
                        item:Items,
                          user: User,
                          importantce: Annotated[int, Body(gt=0)],
                          q:str | None=None

                          
                          ):
    result = {'item_id':item, 'user_id':user_id, 'user':user}
    return result


@app.put("/register/{user_id}")
async def register_user(user_id: int, item: Annotated[Items, Body(embed=True)]):
    result = {'item_id':item, 'user_id':user_id, }
    return result



@app.post("/create/")
async def create(offer: Offer):
    return offer





@app.put("/event/{event_id}")
async def event(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }



@app.post('/user/',response_model=Items)
async def create_item(user: Items):
    return user



class User(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None

    @app.post('/create_user/')
    async def create_user(user: User) -> User:
        return user
    
studentmain = [
    {"name": "Alice"},
    {"name": "Bob"},
    {"name": "Charlie"},
    {"name": "David"},
    {"name": "Eva"},
    {"name": "Frank"},
    {"name": "Grace"},
    {"name": "Hannah"},
    {"name": "Ivy"},
    {"name": "Jack"}
]
@app.get('/students/{student_name}')
async def check(student_name: str):
    for students in studentmain:
        if students['name'] == student_name:
            return {'student': students}
    raise HTTPException(status_code=404, detail='item not found')

@app.exception_handler(StarletteHTTPException)
async def htpp_errror_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/goods/{item_id}")
async def goods(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}





oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.get('/usertoken/')
async def usertoken(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}


def token_user(token):
    return User(username=token + "ekek", 
                email="dkkd,
            full_name="olisa macaulay"
                )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = token_user(token)
    return user


@app.get('/user/me')
async def user_read_me(currentuser: Annotated[User, Depends(get_current_user)]):
    return currentuser
    

fake_users_db = {
    "skyline": {
        "username": "skyline",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "monoskey": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": True,
        
    },
}


class User2(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None


def passwordhash(password:str):
    return "fakehashed" + password



class UserInDB(User2):
    hashed_password: str


def get_user(database, username: str):
    if username in database:
        user_dict = database[username]
        return  UserInDB(**user_dict)




def decode_token(token):
    user = get_user(fake_users_db, token)
    return user

#   return User2(
#             username=user.username,
#             email=user.email,
#             full_name=user.full_name,
#             disabled=user.disabled,
#         )




async def get_currentuser(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    print(user)
    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalide authenication credent",
        headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_active_user(current_users: Annotated[User2, Depends(get_currentuser)]):
    if current_users.disabled:
        raise HTTPException(status_code=400, detail='inactrive user')
    return current_users




@app.post('/token/')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    
    if not user_dict:
        print("User not found.")
        raise HTTPException(status_code=401,detail='username is incorrect')
    user = UserInDB(**user_dict)
    passhas = passwordhash(form_data.password)
    print(f"Hashed Password: {passhas}, Stored Password: {user.hashed_password}")
    if  not passhas == user.hashed_password:
          raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

    
@app.get('/user/me')
async def userlogin(current_user: Annotated[User2, Depends(get_currentuser)]):
    return current_user



SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

fake_users_db = {
    "monoskey": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_type: str | None=None
    token_type: str  | None=None


class tokendata(BaseModel):
    username: str  | None=None


class User(BaseModel):
    username: str
    email: str | None=None
    full_name: str | None=None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)


def has_userpassword(password):
    return pwd_context.hash(password)

def get_user(database, username: str):
    if username in database:
        username_dict = database [username]
        return UserInDB(**username_dict)


def authenticate_user(database, username:str, password: str):
    user= get_user(database,username )
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
          return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = Token(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user



async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]







#create database for all or models













@app.get('/student_list/{student_id}')
def student_list(student_id:  int, session: SessionDB) -> Hero:
    students = session.get(Hero, student_id)
    if not students:
        raise HTTPException(status_code=404, detail='students with the id not found')

    return students


