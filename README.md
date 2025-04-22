# Recount

## Install requirements
pip install -r requirements.txt

## Put all the packages into requirements.txt
pip freeze > requirements.txt

## Run the backend
uvicorn app.main:app --reload

## Check API usage
http://localhost:8000/docs

http://localhost:8000/redocs

## Create tables
scripts/schema.sql