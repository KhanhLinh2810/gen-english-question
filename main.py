from fastapi import FastAPI, Request, HTTPException


from src.routers.public.public import router
from src.utils.response import handler_error
    
app = FastAPI()
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return handler_error(exc)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return handler_error(exc)

@app.get('/check-health')
def check_health():
    return {"status": "ok"}

app.include_router(router)

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)