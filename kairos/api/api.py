from fastapi import APIRouter

from kairos.api.endpoints import object_store

api_router = APIRouter()

api_router.include_router(object_store.router, prefix="/object-store", tags=["object_stores"])
