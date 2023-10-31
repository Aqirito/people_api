from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

from app.api import person_handler, persons_handler
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(persons_handler.router, prefix="/persons", tags=["persons"])
app.include_router(person_handler.router, prefix="/person", tags=["person"])
