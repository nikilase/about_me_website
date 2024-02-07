from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.dependencies import server_config
from app.dependencies import templates

app = FastAPI()
app.add_middleware(
	TrustedHostMiddleware, allowed_hosts=server_config["allowed_hosts"]
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root(request: Request):
	return templates.TemplateResponse("root.html", {"request": request})
