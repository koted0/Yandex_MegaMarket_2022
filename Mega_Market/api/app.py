from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def hello(limit:int):
    return {"limit": f'specified limit parameter = {limit}'}
