from fastapi import Depends, FastAPI

from app.api.endpoints import router
from app.conf.settings import settings
from app.db.session import get_async_session

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(
    router,
    prefix=settings.API_STR,
    dependencies=[Depends(get_async_session)],
)
