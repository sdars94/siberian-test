from typing import Sequence

from sqlalchemy import Row

from app.schemas.invoices import DataOut, Invoice, InvoiceLine


def serialize_invoices(data: Sequence[Row]) -> DataOut:
    """
    Serialize the given invoices data into a DataOut object.

    Args:
        data (Sequence[Row]): The input data containing invoice information.

    Returns:
        DataOut: The output data.
    """

    if not data:
        return DataOut()
    invoices = []
    current_invoice: Invoice | None = None
    invoices_total_out = None
    for row in data:
        (
            title,
            subtotal,
            total,
            line_title,
            quantity,
            price_per_one,
            subtotal_line,
            total_line,
            invoices_total,
        ) = row
        if not invoices_total_out:
            invoices_total_out = invoices_total

        if not current_invoice or current_invoice.title != title:
            current_invoice = Invoice(
                title=title,
                subtotal=subtotal,
                total=total,
                lines=[],
            )
            invoices.append(current_invoice)
        current_invoice.lines.append(
            InvoiceLine(
                title=line_title,
                quantity=quantity,
                price_per_one=price_per_one,
                subtotal_line=subtotal_line,
                total_line=total_line,
            )
        )
    data_out = DataOut(
        invoices=invoices,
        invoices_count=len(invoices),
        invoices_total=invoices_total_out,
    )
    return data_out
