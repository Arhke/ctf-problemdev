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
attempts = 0
chars = string.ascii_letters + string.digits
user = "".join(random.choice(chars) for _ in range(4))
password = "".join(random.choice(chars) for _ in range(3))
passHASH = SHA256.new(data=password.encode()).hexdigest()
# --- Request Models ---
class PasswordInput(BaseModel):
    password: str

flagAttempts = 0
# --- Routes ---
@app.get("/flag")
def flag(username: str, password: str):
    if(username == user and SHA256.new(data=password.encode()).hexdigest() == passHASH):
        flagAttempts += 1
        if flagAttempts > 1:
            return FLAG
        else:
            return None
    flagAttempts = 0
    return None


@app.get("/forgetpass")
def hash(username: str):
    global attempts
    if(username == user):
        attempts +=1
    else:
        attempts = 0
        return {}
    if(attempts > 10000):
        return {"UnsaltedPasswordHash": passHASH}
    return {}

# --- Static Frontend ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
