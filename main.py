from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy import func

# DATABASE

# used for creating a new entry
class HashEntryBase(SQLModel):
    name_hash: str | None = Field(min_length=64, max_length=64)
    email_hash: str | None = Field(min_length=64, max_length=64)
    birthdate_hash: str | None = Field(min_length=64, max_length=64)
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
    birthdate_hash: bool = False
    nationality_hash: bool = False
    comments: list[Comment] | None = None


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

# API

app = FastAPI()

@app.on_event("startup") # needs to be changed
def on_startup():
    create_db_and_tables()

@app.post("/entries/")
def add_entry(entry: HashEntryBase, session: SessionDep) -> HashEntry:
    db_entry = HashEntry.model_validate(entry)
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@app.post("/entries/check")
def check_entries(entries: list[HashEntryRequest], session: SessionDep) -> list[HashEntryResponse]:
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

        # collect the comments of the collected ids
        for id in id_s:
            result = session.exec(select(HashEntry.comment, HashEntry.origin).where(HashEntry.id == id)).first()
            comments.append(Comment(text=result.comment, origin=result.origin))

        resp.comments = comments
        entries_response.append(resp)
    return entries_response