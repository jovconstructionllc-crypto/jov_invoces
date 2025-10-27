from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(300))

    invoices = db.relationship("Invoice", back_populates="client")

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    notes = db.Column(db.Text)
    doc_type = db.Column(db.String(30), default='invoice')

    client = db.relationship("Client", back_populates="invoices")
    lines = db.relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

    def total(self):
        return sum([l.subtotal() for l in self.lines])

class InvoiceLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    description = db.Column(db.String(300), nullable=False)
    qty = db.Column(db.Float, default=1)
    unit_price = db.Column(db.Float, default=0.0)

    invoice = db.relationship("Invoice", back_populates="lines")

    def subtotal(self):
        return (self.qty or 0) * (self.unit_price or 0)
