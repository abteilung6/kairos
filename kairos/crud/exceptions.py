class DatabaseError(Exception):
    """General Database error"""

class EntityNotFoundError(DatabaseError):
    """The entity does not exist."""

