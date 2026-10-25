from .security.api_key_check import verify_internal_key
from .routers.run_process import render
from .routers.examples import router as examples_router
from .routers.scripts import router as scripts_router
from .routers.sources import router as sources_router
from .routers.minio import router as minio_router

from pathlib import Path
from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(minio_router)
app.include_router(examples_router)
app.include_router(scripts_router)
app.include_router(sources_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/data")
async def get_data(
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)

    return {
        "message": "Hello from FastAPI"
    }

@app.get("/api/{filename}")
async def get_file(
    filename: str,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    input_file = str(Path.cwd()  / f"{filename}.md")
    output_file = str(Path.cwd() / f"{filename}.html")
    command = ["pandoc", input_file, "-o", output_file]
    await render(command)
    with open(output_file, "r") as f:
        html = f.read()
    return HTMLResponse(content=html)