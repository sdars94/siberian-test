from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy declarative models.

    This class extends SQLAlchemy's DeclarativeBase and provides common
    attributes and methods for declarative models.

    Generates the table name automatically based on the lowercase name of
    the model.

    Attributes:
        id (Mapped[int]): The primary key for the model, auto-incremented.
        __name__ (str): The name of the model.
    """

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    __name__: str

    # Generate __tablename__ automatically
    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
