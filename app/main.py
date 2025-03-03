import secrets

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.dependencies import server_config, templates

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=server_config["allowed_hosts"])
app.mount("/static", StaticFiles(directory="static"), name="static")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        nonce = secrets.token_hex(16)
        request.state.nonce = nonce
        response: Response = await call_next(request)
        csp = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            f"style-src 'self' https://cdn.jsdelivr.net https://fonts.googleapis.com 'nonce-{nonce}'; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
            "img-src 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "frame-ancestors 'self'; "
            "connect-src 'self'; "
            "media-src 'self'; "
            "frame-src 'self'; "
            "worker-src 'self'; "
            "manifest-src 'self';"
        )
        response.headers["Content-Security-Policy"] = csp.encode('ascii', 'ignore').decode('ascii')
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


app.add_middleware(SecurityHeadersMiddleware)


@app.get("/")
async def root(request: Request):
    nonce = request.state.nonce
    return templates.TemplateResponse("root.html", {"request": request, "nonce": nonce})


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon/favicon.ico")


@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt", media_type="text")
