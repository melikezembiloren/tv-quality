from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Tüm SQLAlchemy ORM modellerinin türediği ortak temel sınıf."""
    pass
