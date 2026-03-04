from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, ocr

app = FastAPI(title="HealthNet API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(ocr.router, prefix="/api/ocr", tags=["ocr"])


