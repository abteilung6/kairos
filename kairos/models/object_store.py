from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from kairos.db.base import Base


class ObjectStore(Base):
    __tablename__ = "object_stores"

    id = Column(UUID(as_uuid=True), primary_key=True)
    object_key = Column(String, unique=True)
    claimed_time = Column(DateTime)
    occupied_time = Column(DateTime, default=None, nullable=True)
    bucket_get_url = Column(String)
