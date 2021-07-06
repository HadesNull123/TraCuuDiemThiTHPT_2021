from fastapi import FastAPI
from core.getdiem import TraCuuDiemThi

app = FastAPI()

@app.router("/")
async def getdiem():
    pass