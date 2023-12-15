VERSION 0.7
FROM python:3.12-slim-bookworm

WORKDIR excel2xx


publish:
    FROM python:3.12-slim-bookworm
    COPY ./  ./
 

tests:
    FROM python:3.12-slim-bookworm
    RUN pip install tox
    RUN tox
    COPY .  .
    RUN tox 
    
