from uuid import UUID

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from config import Config
from kairos import crud, schemas
from kairos.api.deps import get_aws_cloud_caller, get_db, get_environment_config
from kairos.cloud.aws import AWSCaller, generate_object_key
from kairos.schemas.object_store import (
    ObjectStore,
    ObjectStoreCreateRequest,
    ObjectStoreCreateResponse,
    ObjectStoreListResponse,
    ObjectStoreState,
    ObjectStoreUpdateRequest,
)
from kairos.utils.date import now

router = APIRouter()


@router.get(
    "/",
    response_model=ObjectStoreListResponse,
    status_code=status.HTTP_200_OK,
    summary="Return a list of object stores.",
    response_description="List of objects stores.",
)
def object_store_list(
    db: Session = Depends(get_db),
) -> ObjectStoreListResponse:
    object_stores = crud.object_store_list(db=db)
    return ObjectStoreListResponse(object_stores=object_stores)


@router.post(
    "/",
    response_model=ObjectStoreCreateResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a presigned url for object storage.",
    description="Generate a presigned url in order to upload your file to object store.",
    response_description="Object meta data including the generated presigned url.",
)
def object_store_create(
    request: ObjectStoreCreateRequest,
    cloud_caller: AWSCaller = Depends(get_aws_cloud_caller),
    config: Config = Depends(get_environment_config),
    db: Session = Depends(get_db),
) -> ObjectStoreCreateResponse:
    object_key = generate_object_key(request.file_name)
    try:
        presigned_post_response = cloud_caller.create_presigned_post(
            bucket_name=config.BUCKET_NAME,
            key=object_key,
        )
    except ClientError as ex:
        logger.error(f"Operation create_presigned_post failed, ex: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fully process this request because of an internal server error.",
        ) from ex

    db_object_store = crud.object_store_create(
        db=db,
        obj=schemas.ObjectStoreCreate(
            object_key=object_key,
            claimed_time=now(),
            occupied_time=None,
            bucket_get_url=None,
        ),
    )

    return ObjectStoreCreateResponse(
        id=db_object_store.id,
        object_key=db_object_store.object_key,
        claimed_time=db_object_store.claimed_time,
        occupied_time=db_object_store.occupied_time,
        bucket_get_url=db_object_store.bucket_get_url,
        bucket_post_url=presigned_post_response.url,
        fields=presigned_post_response.fields,
    )


@router.patch(
    "/{object_store_id}",
    response_model=ObjectStore,
    status_code=status.HTTP_200_OK,
    summary="Update object store.",
    description="Acknowledge that object key was uploaded.",
)
def object_store_update(
    object_store_id: UUID,
    request: ObjectStoreUpdateRequest,
    db: Session = Depends(get_db),
    cloud_caller: AWSCaller = Depends(get_aws_cloud_caller),
    config: Config = Depends(get_environment_config),
) -> ObjectStore:
    db_object_store = crud.object_store_get_by_object_id(db=db, id=object_store_id)
    if not db_object_store:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Object store not found.")
    current_object_store = ObjectStore.model_validate(db_object_store)
    _validate_object_store_state_transition(current_object_store, request.state)

    try:
        presigned_get_url = cloud_caller.create_presigned_get_url(
            bucket_name=config.BUCKET_NAME,
            key=db_object_store.object_key,
        )
    except ClientError as ex:
        logger.error(f"Failed to receive presigned get url, ex: {ex}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fully process this request because of an internal server error.",
        ) from ex

    updated_db_object_store = crud.object_store_update_by_object_id(
        db=db, id=db_object_store.id, occupied_time=now(), bucket_get_url=presigned_get_url,
    )

    return ObjectStore.model_validate(updated_db_object_store)

def _validate_object_store_state_transition(current_object_store: ObjectStore, target_state: ObjectStoreState) -> None:
    if target_state != ObjectStoreState.occupied and current_object_store.state != ObjectStoreState.claimed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Requested target object store state {target_state} is not allowed.",
        )
