from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from itsdangerous import Signer
import base64
import os
import logging
from Cryptodome.Hash import SHA256
import random
import string

app = FastAPI()
sessions = {}

SERVER_SECRET_KEY = os.environ.get("SEED")
if SERVER_SECRET_KEY is None:
    print("Server secret key not set. Picking random value.")
    SERVER_SECRET_KEY=os.urandom(32)

assert len(SERVER_SECRET_KEY) == 32  # Must be for AES-256

signer = Signer(SERVER_SECRET_KEY) 

logger = logging.getLogger("uvicorn")


# Load flag once
FLAG=""
with open("/challenge/flag", "r") as f:
    FLAG = f.read().strip()

chars = string.ascii_letters + string.digits
HASH = SHA256.new(data=b'test.').hexdigest()
# HASH = SHA256.new(data=''.join(random.choice(chars) for _ in range(5)).encode()).hexdigest()

# --- Request Models ---
class PasswordInput(BaseModel):
    password: str


# --- Routes ---
@app.get("/flag")
def flag(password: str):
    if(SHA256.new(data=password.encode()).hexdigest() == HASH):
        return FLAG
    return None


@app.get("/hash")
def hash(request: Request):
    return {"UnsaltedPasswordHash": HASH}

# --- Static Frontend ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
