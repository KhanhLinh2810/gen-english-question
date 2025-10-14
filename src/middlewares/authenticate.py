from fastapi import Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from env import config
from src.loaders.database import get_db
from src.services.user import get_user_service

async def authenticate(request: Request, db: AsyncSession = Depends(get_db), user_service = Depends(get_user_service)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="token_invalid")

    token = auth_header.split("Bearer")[1].strip()
    payload = jwt.decode(token, config["jwt"]["secret_key"], algorithm=config["jwt"]["algorithm"])
    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="token_invalid")

    user = await user_service.find_by_pk(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="token_invalid")
    request.state.user = user

