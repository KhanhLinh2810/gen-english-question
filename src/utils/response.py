from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse

import math
import logging

logger = logging.getLogger(__name__)

def res_ok(data: dict = None, code: str = "SUCCESS",
           page: int = None, limit: int = None, total_items: int = None):

    response = {
        "code": code,
        "message": code,
        "data": data or {}
    }

    if page is not None and limit is not None and total_items is not None:
        total_pages = int(total_items/limit)
        response["meta"] = {
            "total_pages": total_pages,
            "total_items": total_items,
            "limit": limit,
            "page": page
        }

    return response


def handler_error(error: Exception) -> JSONResponse:
    status_code = getattr(error, 'status_code', 500)
    detail = getattr(error, 'detail', str(error))

    logger.error(f"Exception occurred: {detail}", exc_info=True)

    return JSONResponse(
        status_code=status_code,
        content={"message": detail,}
    )
