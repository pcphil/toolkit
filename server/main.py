from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routers import base64, converter, hasher

app = FastAPI(title="Toolkit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1420", "tauri://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base64.router)
app.include_router(hasher.router)
app.include_router(converter.router)


@app.get("/health")
def health():
    return {"status": "ok", "tools": ["base64", "hasher", "converter"]}
