from fastapi import Request, HTTPException, Depends

import jwt
from env import config

async def authenticate(request: Request):
    if config["app"]['ignore_authen']:
        return
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="token_invalid")

    token = auth_header.split("Bearer")[1].strip()
    payload = jwt.decode(token, config["jwt"]["secret_key"], algorithm=config["jwt"]["algorithm"])
    server_id = payload.get("id")
    if server_id != config["app"]["server_id"]:
        raise HTTPException(status_code=401, detail="token_invalid")

