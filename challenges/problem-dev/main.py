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

assert len(SERVER_SECRET_KEY) == 32
signer = Signer(SERVER_SECRET_KEY) 
logger = logging.getLogger("uvicorn")


# Load flag once
FLAG=""
with open("/challenge/flag", "r") as f:
    FLAG = f.read().strip()
attempts = 0
def getHash(string): #Sha256 Truncates :( 
    for _ in range(len(string)):
        string = SHA256.new(data=string.encode()).hexdigest()
    return string
chars = string.ascii_letters + string.digits
user = "".join(random.choice(chars) for _ in range(2))
password = "".join(random.choice(chars) for _ in range(25))
passHASH = getHash(password)
print(user, password, "====================================")
# --- Request Models ---


flagAttempts = 0
# --- Routes ---
@app.get("/flag")
def flag(username: str, password: str):
    print(username[0:5], password[0:5])

    if(username == user and getHash(password) == passHASH):
        return FLAG
    return None


@app.get("/forgetpass")
def hash(username: str):
    global user
    global password
    global passHASH    
    if(username == user):
        #set the password to something simple
        password = "".join(random.choice(chars) for _ in range(2))
        passHASH = getHash(password)
        return {"UnsaltedPasswordHash": passHASH}
    # Hm... is somebody trying to abuse our password forget system? Nein.
    user = "".join(random.choice(chars) for _ in range(2))
    fakePassword = "".join(random.choice(chars) for _ in range(25))
    return {"UnsaltedPasswordHash": getHash(fakePassword)}

# --- Static Frontend ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
