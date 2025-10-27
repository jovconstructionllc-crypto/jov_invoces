from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Optional

class ClientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Optional()])
    phone = StringField("Phone", validators=[Optional()])
    address = TextAreaField("Address", validators=[Optional()])
    submit = SubmitField("Save")

class InvoiceForm(FlaskForm):
    number = StringField("Document Number", validators=[DataRequired()])
    date = DateField("Date", validators=[Optional()])
    due_date = DateField("Due Date", validators=[Optional()])
    client_id = IntegerField("Client ID", validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional()])
    submit = SubmitField("Create Document")
