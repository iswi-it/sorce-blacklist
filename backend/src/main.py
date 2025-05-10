from typing import Annotated
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import func
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError

import jwt
import os

# Environment variables

SECRET_KEY = os.getenv("SECRTE_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

INITIAL_USERNAME = os.getenv("INITIAL_USERNAME", "iswi")
INITIAL_CONFERENCE = os.getenv("INITIAL_CONFERENCE", "ISWI")
INITIAL_PASSWORD = os.getenv("INITIAL_PASSWORD", "password123")

REGISTRATION_SECRET = os.getenv("REGISTRATION_SECRET", "1")

# DATABASE

# used for creating a new entry
class HashEntryBase(SQLModel):
    name_hash: str | None = Field(min_length=64, max_length=64)
    email_hash: str | None = Field(min_length=64, max_length=64)
    birthdate_hash: str | None = Field(min_length=64, max_length=64)
    nationality_hash: str | None = Field(min_length=64, max_length=64)
    origin: str
    comment: str | None

# id is only used internally
class HashEntry(HashEntryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# fields used for a request towards the blacklist
class HashEntryRequest(BaseModel):
    name_hash: str | None
    email_hash: str | None
    birthdate_hash: str | None
    nationality_hash: str | None

class Comment(BaseModel):
    text: str | None
    origin: str | None

# structure of response, for each given hash a boolean is returned if it can be found in the list + the corresponding comment
class HashEntryResponse(BaseModel):
    name_hash: bool = False
    email_hash: bool = False
    nationality_hash: bool = False
    birthdate_hash: bool = False
    comments: list[Comment] | None = None

# information of a user of the system
class User(SQLModel):
    username: str | None = Field(default=None, primary_key=True)
    conference: str

# model to create a new user, with plain password
class UserCreate(User):
    password: str
    registration_secret: str

# db internal information of a user
class UserInDB(User, table=True):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Statistics(BaseModel):
    num: int = 0
    conferences: list[str] = None


pwd_context = CryptContext(schemes=["bcrypt"])


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain: str, hash: str):
    return pwd_context.verify(plain, hash)

def get_password_hash(plain: str):
    return pwd_context.hash(plain)

def get_user(username: str, session: SessionDep) -> (UserInDB | None):
    return session.exec(select(UserInDB).where(UserInDB.username == username)).first()

def authenticate_user(username: str, password: str, session) -> (UserInDB | bool):
    user = get_user(username, session)
    if user == None:
        return False
    if not verify_password(password, user.password):
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

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user

# API

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup") # needs to be changed
def on_startup():
    create_db_and_tables()

    # check if a user is existing, if not create default user
    with Session(engine) as session:
        users = session.exec(select(UserInDB)).first()
        if not users:
            init_user = UserInDB(
                username=INITIAL_USERNAME,
                password=get_password_hash(INITIAL_PASSWORD),
                conference=INITIAL_CONFERENCE
            )
            session.add(init_user)
            session.commit()
            print("Initial user created!")

@app.post("/entries/")
def add_entry(entry: HashEntryBase, token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> HashEntry:
    db_entry = HashEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@app.get("/statistics")
def statistics(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> Statistics:
    statistics = Statistics(num = session.exec(select(func.count(HashEntry.id))).one(), conferences = session.exec(select(UserInDB.conference)))
    return statistics

@app.post("/entries/check")
def check_entries(entries: list[HashEntryRequest], token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> list[HashEntryResponse]:
    entries_response = list()
    for entry in entries:
        resp = HashEntryResponse()
        id_s = set()
        comments = list()

        # check for all hashes if they occur in some row and collect the ids

        if (session.exec(select(func.count(HashEntry.id)).where(HashEntry.name_hash == entry.name_hash)).first() > 0):
            resp.name_hash = True
            id_s.update(session.exec(select(HashEntry.id).where(HashEntry.name_hash == entry.name_hash)).all())

        if (session.exec(select(func.count(HashEntry.id)).where(HashEntry.email_hash == entry.email_hash)).first() > 0):
            resp.email_hash = True
            id_s.update(session.exec(select(HashEntry.id).where(HashEntry.email_hash == entry.email_hash)).all())

        if (session.exec(select(func.count(HashEntry.id)).where(HashEntry.birthdate_hash == entry.birthdate_hash)).first() > 0):
            resp.birthdate_hash = True
            id_s.update(session.exec(select(HashEntry.id).where(HashEntry.birthdate_hash == entry.birthdate_hash)).all())

        if (resp.name_hash or resp.email_hash or resp.birthdate_hash): # only when one is true check for the nationality
            if (session.exec(select(func.count(HashEntry.id)).where(HashEntry.nationality_hash == entry.nationality_hash)).first() > 0):
                resp.nationality_hash = True

        # collect the comments of the collected ids
        for id in id_s:
            result = session.exec(select(HashEntry.comment, HashEntry.origin).where(HashEntry.id == id)).first()
            comments.append(Comment(text=result.comment, origin=result.origin))

        resp.comments = comments
        entries_response.append(resp)
    return entries_response


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@app.post("/users/")
async def create_user(user: UserCreate, session: SessionDep) -> User:
    # authenticate with token
    if user.registration_secret != REGISTRATION_SECRET:
        raise HTTPException(status_code=400, detail="Incorrect registration token")

    # check if user is already existing
    existing = session.exec(select(UserInDB).where(UserInDB.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    # create user
    password_hash = get_password_hash(user.password)
    db_user = UserInDB(username=user.username, conference=user.conference, password=password_hash)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

