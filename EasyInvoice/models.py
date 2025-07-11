from . import db

class Client(db.Model):
    """Represents a client company"""
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True, index=True)
    company = db.Column(db.String, nullable=False)
    company_code = db.Column(db.Integer, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)

    invoices = db.relationship("Invoice", back_populates="client")

    def __str__(self) -> str:
        return f"{self.company} - {self.company_code}"

class Invoice(db.Model):
    """Represents invoices"""
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True, index=True)
    invoice_no = db.Column(db.String, unique=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)

    client = db.relationship("Client", back_populates="invoices")
    items = db.relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")

    def __str__(self):
        return self.invoice_no
    
class InvoiceItem(db.Model):
    """Represents invoice items"""
    __tablename__ = "invoice_items"

    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    sum = db.Column(db.Float, nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)

    invoice = db.relationship("Invoice", back_populates="items")

class Provider(db.Model):
    """Represents a service Provider"""
    __tablename__ = "providers"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    idv_no = db.Column(db.Integer, nullable=False)
    bank = db.Column(db.String, nullable=False)
    account_no = db.Column(db.String, nullable=True)
