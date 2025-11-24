FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10


ARG FLAG="CTF{default_flag}"
ARG SEED="insecure_default_seed"

RUN install -d -m 0700 /challenge/
COPY setup-challenge.py /challenge/setup-challenge.py
RUN python3 /challenge/setup-challenge.py

WORKDIR /app
COPY ./main.py /app/main.py
COPY ./static /app/static
COPY requirements.txt .
RUN pip install -r requirements.txt



# * Creates /challenge/artifacts.tar.gz which cmgr uses to offer artifact
#   downloads in problem.md.
# * Creates /challenge/metadata.json which defines the flag and potentially
#   other metadata.
RUN tar czvf /challenge/artifacts.tar.gz main.py 

# Expose the port on which the Flask app will run
EXPOSE 8000

# PUBLISH 8000 AS HTTP
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

