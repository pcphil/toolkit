import hashlib
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

SUPPORTED = ("md5", "sha1", "sha256", "sha512")

router = APIRouter(prefix="/api/hash", tags=["hash"])


@router.post("/")
async def hash_file(
    file: UploadFile = File(...),
    algorithm: str = Form("sha256"),
):
    if algorithm not in SUPPORTED:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported algorithm '{algorithm}'. Choose from: {', '.join(SUPPORTED)}",
        )

    h = hashlib.new(algorithm)
    while chunk := await file.read(8192):
        h.update(chunk)

    return {
        "filename": file.filename,
        "algorithm": algorithm,
        "digest": h.hexdigest(),
    }
