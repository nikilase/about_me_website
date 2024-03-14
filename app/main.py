from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.dependencies import server_config, templates

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=server_config["allowed_hosts"])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon/favicon.ico")


@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt", media_type="text")
