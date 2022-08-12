from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from os.path import join, dirname, realpath
from fastapi.middleware.cors import CORSMiddleware
import os

from .api import router

app = FastAPI(
    title='Online Shop Bot Backend',
)

os.environ["TMPDIR"] = os.getcwd()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router)
app.mount("/static", StaticFiles(directory=join(dirname(realpath(__file__)), "static")), name="static")