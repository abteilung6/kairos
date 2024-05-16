from datetime import datetime
from enum import Enum, unique
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, computed_field

from kairos.cloud.schemas import PresignedFields


@unique
class ObjectStoreState(str, Enum):
    claimed = "claimed"
    occupied = "occupied"


class ObjectStoreBase(BaseModel):
    object_key: str
    claimed_time: datetime
    occupied_time: datetime | None
    bucket_get_url: HttpUrl | None = Field(
        title="A generated presigned Get URL",
        description="Using a presigned URL will allow an object retrieval without requiring another party to have AWS security credentials or permissions.",  # noqa: E501
    )

    @computed_field
    @property
    def state(self) -> ObjectStoreState:
        if self.occupied_time:
            return ObjectStoreState.occupied
        return ObjectStoreState.claimed


class ObjectStoreCreate(ObjectStoreBase): ...


class ObjectStore(ObjectStoreBase):
    id: UUID

    class Config:
        from_attributes = True


class ObjectStoreUpdateRequest(BaseModel):
    state: ObjectStoreState


class ObjectStoreCreateRequest(BaseModel):
    file_name: str = Field(
        title="Name of the file that gets upload to the bucket key",
        examples=["sample.png"],
    )


class ObjectStoreCreateResponse(ObjectStore):
    bucket_post_url: HttpUrl | None = Field(
        title="A generated presigned Post URL",
        description="Using a presigned URL will allow an upload without requiring another party to have AWS security credentials or permissions.",  # noqa: E501
    )
    fields: PresignedFields  # only exposed during creation
