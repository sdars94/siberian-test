import decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Invoice(Base):
    """
    A class representing an Invoice.

    Attributes:
         title (str): The title of the invoice.
         discount (Numeric): The discount applied to the invoice.
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
    A class representing a Line in the Invoice.

    Attributes:
        title (str): The title of the invoice line.
        quantity (int): The quantity of the item.
        price_per_one (Decimal): The price per unit of the item.
        invoice_id (int): The ID of the associated invoice.
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
