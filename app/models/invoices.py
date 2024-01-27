import decimal

from sqlalchemy import ForeignKey, String
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Invoice(Base):
    """
    Invoice class.

    Represents an Invoice in the system.
    """

    title: Mapped[str] = mapped_column(String(255), unique=True)
    discount = mapped_column(Numeric(precision=10, scale=2))

    def __repr__(self):
        return (
            f"Invoice: id={self.id}, title={self.title}, "
            f"discount={self.discount}"
        )


class InvoiceLine(Base):
    """
    InvoiceLine class.

    Represents a Line in the Invoice in the system.
    """

    title: Mapped[str]
    quantity: Mapped[int]
    price_per_one: Mapped[decimal.Decimal] = mapped_column(
        Numeric(precision=10, scale=2)
    )
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoice.id", ondelete="CASCADE"), index=True
    )

    def __repr__(self):
        return (
            f"InvoiceLine: id={self.id}, title={self.title}, "
            f"quantity={self.quantity}, price_per_one={self.price_per_one}"
        )
