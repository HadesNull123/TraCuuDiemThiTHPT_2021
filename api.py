from fastapi import FastAPI
from utils.getdiem import TraCuuDiemThi

app = FastAPI()

@app.router("/")
async def getdiem():
    pass