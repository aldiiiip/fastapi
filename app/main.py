#Set-ExecutionPolicy Unrestricted -Scope Process
#venv\Scripts\Activate.ps1
#uvicorn main:app

from fastapi import FastAPI
from . import models
from .database import engine
from .database import SessionLocal
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")   #sending get request to API
def root():
    return {"message": "Welcome to my API server! test"}




