from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.

    - This class acts as the foundation for all database models.
    - It enables automatic table creation and inheritance for future models.
    """
    pass
