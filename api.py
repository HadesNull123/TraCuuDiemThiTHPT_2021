from fastapi import FastAPI
from lib.getdiem import TraCuuDiemThi

app = FastAPI()

@app.router("/")
async def getdiem():
    pass