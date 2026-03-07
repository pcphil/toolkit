import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/base64", tags=["base64"])


class TextPayload(BaseModel):
    text: str


@router.post("/encode")
def encode(payload: TextPayload):
    try:
        result = base64.b64encode(payload.text.encode("utf-8")).decode("utf-8")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/decode")
def decode(payload: TextPayload):
    try:
        result = base64.b64decode(payload.text.encode("utf-8")).decode("utf-8")
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
