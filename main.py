from fastapi import FastAPI

from core.api.endpoints.authentication import auth
from core.api.endpoints.token import token

app = FastAPI()

# Register routers
app.include_router(router=auth, tags=['authentication'], prefix='/auth')
app.include_router(router=token, tags=['token'], prefix='/token')