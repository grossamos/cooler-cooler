from aiohttp.web import middleware, HTTPUnauthorized, HTTPForbidden
import os

CREDENTIAL = os.environ.get("MEROSS_CREDENTIAL")

@middleware
async def auth_middleware(request, handler):
    if "Authorization" not in request.headers:
        raise HTTPUnauthorized();

    credential = request.headers["Authorization"]
    if credential != CREDENTIAL:
        raise HTTPForbidden()

    resp = await handler(request)
    return resp
