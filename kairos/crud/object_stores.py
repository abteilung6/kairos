from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from kairos import models, schemas
from kairos.crud.exceptions import EntityNotFoundError


def object_store_create(db: Session, obj: schemas.ObjectStoreCreate) -> models.ObjectStore:
    db_object_store = models.ObjectStore(
        id=uuid4(),
        object_key=obj.object_key,
        claimed_time=obj.claimed_time,
        occupied_time=obj.occupied_time,
        bucket_get_url=str(obj.bucket_get_url) if obj.bucket_get_url else None,
    )
    db.add(db_object_store)
    db.commit()
    db.refresh(db_object_store)
    return db_object_store


def object_store_get_by_object_id(db: Session, id: UUID) -> models.ObjectStore | None:
    return db.query(models.ObjectStore).filter(models.ObjectStore.id == id).first()


def object_store_update_by_object_id(
    db: Session, id: UUID, occupied_time: datetime | None, bucket_get_url: str | None,
) -> models.ObjectStore:
    db_object_store = db.query(models.ObjectStore).filter(models.ObjectStore.id == id).first()
    if not db_object_store:
        raise EntityNotFoundError(f"Object store with id {id} does not exist.")
    if occupied_time:
        db_object_store.occupied_time = occupied_time
    if bucket_get_url is not None:
        db_object_store.bucket_get_url = bucket_get_url
    db.commit()
    db.refresh(db_object_store)
    return db_object_store
