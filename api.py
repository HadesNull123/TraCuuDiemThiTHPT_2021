from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from utils.getdiem import TraCuuDiemThi


class GetInfo(BaseModel):
    sbd: str
    year: int = Query(..., ge=2019, le=2021)


app = FastAPI()


@app.post("/lksjdakw", status_code=200)
async def lay_diem_thi(get_info: GetInfo):
    tracuu = TraCuuDiemThi(year=str(get_info.year), sbd=get_info.sbd)

    if tracuu.diem_thi_24h():
        return {"mess": tracuu.result}
    elif tracuu.diem_thi_thptquocgia():
        return {"mess": tracuu.result}
    elif tracuu.diem_thi_thptquocgia():
        return {"mess": tracuu.result}
    else:
        tracuu.diem_thi_vietnamnet()
        return {"mess": tracuu.result}
