from pydantic import BaseModel


class InvoiceLine(BaseModel):
    title: str
    quantity: int
    price_per_one: float
    subtotal_line: float
    total_line: float


class Invoice(BaseModel):
    title: str
    subtotal: float
    total: float
    lines: list[InvoiceLine] = []


class DataOut(BaseModel):
    invoices: list[Invoice | None] = []
    invoices_count: int = 0
    invoices_total: float = 0
