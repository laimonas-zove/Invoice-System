from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, IntegerField, TextAreaField, FloatField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Optional
from .models import Client, Invoice

class ClientForm(FlaskForm):
    company = StringField('Įmonė', validators=[DataRequired()])
    company_code = IntegerField('Įmonės Kodas', validators=[DataRequired()])
    address = StringField('Adresas', validators=[DataRequired()])
    phone_number = StringField('Tel. Numeris', validators=[Optional()])
    email = EmailField('El. Paštas', validators=[DataRequired()])
    submit = SubmitField('Patvirtinti')

class InvoiceItemForm(FlaskForm):
    class Meta:
        csrf = False
        
    service = TextAreaField("Paslauga", validators=[DataRequired()])
    quantity = IntegerField("Kiekis", validators=[DataRequired()])
    price = FloatField("Kaina", validators=[DataRequired()])

class InvoiceForm(FlaskForm):
    client_id = SelectField("Klientas", coerce=int, validators=[DataRequired()])
    items = FieldList(FormField(InvoiceItemForm), min_entries=1)
    submit = SubmitField('Patvirtinti')

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.client_id.choices = [
            (client.id, f"{client.company} - {client.company_code}")
            for client in Client.query.all()]
        
class ProviderForm(FlaskForm):
    name = StringField('Vardas', validators=[DataRequired()])
    surname = StringField('Pavardė', validators=[DataRequired()])
    address = TextAreaField('Adresas', validators=[DataRequired()])
    idv_no = IntegerField('Idv Numeris', validators=[DataRequired()])
    bank = StringField('Bankas', validators=[DataRequired()])
    account_no = StringField('Sąskaitos Numeris', validators=[DataRequired()])
    submit = SubmitField('Patvirtinti')