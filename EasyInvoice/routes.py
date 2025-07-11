import datetime
import os
import io
from . import app, db
from playwright.sync_api import sync_playwright
from threading import Thread
from flask import render_template, Response, flash, redirect, url_for, send_file, request
from .models import Invoice, Client, Provider, InvoiceItem
from .forms import ClientForm, InvoiceForm, ProviderForm
from. utils import amount_to_words

@app.route("/")
def index() -> Response:
    return render_template("index.html")

@app.route("/saskaitos")
def invoices() -> Response:
    invoices = Invoice.query.all()
    show_pdf_invoice_id = request.args.get('show_pdf')
    return render_template("invoices/invoices.html", 
                         invoices=invoices, 
                         show_pdf_invoice_id=show_pdf_invoice_id)

@app.route('/saskaitos/naujas/', methods=["GET", "POST"])
def new_invoice():
    form = InvoiceForm()
    provider = Provider.query.first()
    if not provider:
        flash("Pirmiausia sukurkite Pardavėją", "error")
        return redirect(url_for("invoices"))
        
    client = Client.query.first()
    if not client:
        flash("Pirmiausia sukurkite Klientą", "error")
        return redirect(url_for("invoices"))

    if form.validate_on_submit():
        last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
        invoice_no = f"{(int(last_invoice.invoice_no) + 1):03d}" if last_invoice else "001"

        invoice = Invoice(
            invoice_no=invoice_no,
            date=datetime.date.today(),
            client_id=form.client_id.data,
        )
        db.session.add(invoice)
        db.session.flush()

        for item_form in form.items.entries:
            item = InvoiceItem(
                service=item_form.form.service.data,
                quantity=item_form.form.quantity.data,
                price=item_form.form.price.data,
                sum=item_form.form.quantity.data * item_form.form.price.data,
                invoice_id=invoice.id
            )
            db.session.add(item)

        db.session.commit()
        flash("Sąskaita sukurta", "success")
        return redirect(url_for("invoices", show_pdf=invoice.id))

    return render_template("invoices/add_new.html", form=form)


@app.route('/saskaitos/<int:invoice_id>', methods=["GET", "POST"])
def edit_invoice(invoice_id: int) -> Response:
    invoice = Invoice.query.get_or_404(invoice_id)

    class DynamicFullInvoiceForm(InvoiceForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if request.method == "POST":
                total = 0
                while f"items-{total}-service" in request.form:
                    total += 1
                self.items.min_entries = total
                while len(self.items.entries) < total:
                    self.items.append_entry()
            else:
                self.items.min_entries = len(invoice.items)
                while len(self.items.entries) < len(invoice.items):
                    self.items.append_entry()

    form = DynamicFullInvoiceForm(obj=invoice)

    if request.method == "GET":
        for subform, item in zip(form.items.entries, invoice.items):
            subform.form.service.data = item.service
            subform.form.quantity.data = item.quantity
            subform.form.price.data = item.price

    if form.validate_on_submit():
        invoice.client_id = form.client_id.data

        InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()

        for item_form in form.items.entries:
            new_item = InvoiceItem(
                service=item_form.form.service.data,
                quantity=item_form.form.quantity.data,
                price=item_form.form.price.data,
                sum=item_form.form.quantity.data * item_form.form.price.data,
                invoice_id=invoice.id
            )
            db.session.add(new_item)

        db.session.commit()

        flash("Sąskaita atnaujinta sėkmingai", "success")
        return redirect(url_for("invoices"))

    return render_template("invoices/edit.html", form=form, invoice=invoice)


@app.route("/klientai")
def clients() -> Response:
    clients = Client.query.all()
    return render_template("clients/clients.html", clients=clients)

@app.route('/klientai/naujas/', methods=["GET", "POST"])
def new_client() -> Response:
    form = ClientForm()

    if form.validate_on_submit():
        company = form.company.data
        company_code = form.company_code.data
        existing_client = Client.query.filter_by(company_code=company_code).first()

        if existing_client:
            flash('Įmonė tokiu kodu jau yra duomenų bazėje', 'error')
            return render_template('/clients/add_new.html', form=form)
        
        address = form.address.data
        phone_number = form.phone_number.data
        email = form.email.data

        new_client = Client(
            company=company,
            company_code=company_code,
            address=address,
            phone_number=phone_number,
            email=email
        )

        db.session.add(new_client)
        db.session.commit()

        flash('Klientas Sėkmingai Pridėtas', 'success')
        return redirect(url_for('clients'))

    return render_template('/clients/add_new.html', form=form)

@app.route('/klientai/<int:client_id>', methods=["GET", "POST"])
def edit_client(client_id:int) -> Response:
    client = Client.query.get(client_id)

    if not client:
        flash('Klientas nerastas', 'error')
        return redirect(url_for('clients'))
    
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        client.company = form.company.data
        client.company_code = form.company_code.data
        client.address = form.address.data
        client.phone_number = form.phone_number.data
        client.email = form.email.data

        db.session.commit()

        flash('Kliento informacija sėkmingai atnaujinta', 'success')
        return redirect(url_for('clients'))

    return render_template('clients/edit.html', form=form, client=client)

@app.route('/pardavėjas/', methods=["GET", "POST"])
def provider() -> Response:
    provider = Provider.query.first()

    if not provider:
        form = ProviderForm()

        if form.validate_on_submit():
            name=form.name.data
            surname=form.surname.data        
            address = form.address.data
            idv_no = form.idv_no.data
            bank = form.bank.data
            account_no = form.account_no.data

            if len(form.account_no.data) != 20 or form.account_no.data.lower()[0:2] != 'lt':
                flash('Neteisingas sąskaitos numeris', 'error')
                return render_template('provider.html', form=form)

            new_provider = Provider(
                name=name,
                surname=surname,
                address=address,
                idv_no=idv_no,
                bank=bank,
                account_no=account_no
            )

            db.session.add(new_provider)
            db.session.commit()

            flash('Pardavėjas Sėkmingai Pridėtas', 'success')
            return redirect(url_for('index'))
    
    form = ProviderForm(obj=provider)

    if form.validate_on_submit():
        provider.address = form.address.data
        provider.idv_no = form.idv_no.data
        provider.bank = form.bank.data
        provider.account_no = form.account_no.data

        if len(form.account_no.data) != 20 or form.account_no.data.lower()[0:2] != 'lt':
                flash('Neteisingas sąskaitos numeris', 'error')
                return render_template('provider.html', form=form, provider=provider)

        db.session.commit()

        flash('Pardavėjo duomenys sėkmingai atnaujinti', 'success')
        return redirect(url_for('provider'))

    return render_template('provider.html', form=form, provider=provider)

@app.route("/saskaitos/pdf/<int:invoice_id>")
def generate_invoice(invoice_id: int) -> Response:
    invoice = Invoice.query.filter_by(id=invoice_id).first()
    provider = Provider.query.first()
    total_sum = sum(item.sum for item in invoice.items)
    sum_words = amount_to_words(total_sum)

    html = render_template('invoices/invoice.html', invoice=invoice, provider=provider, sum_words=sum_words, total_sum=total_sum)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html)
            pdf_bytes = page.pdf(
                format='A4',
                margin={'top': '20mm', 'right': '10mm', 'bottom': '20mm', 'left': '20mm'},
                print_background=True,
                scale=0.8
            )
            browser.close()
        
        return send_file(
            io.BytesIO(pdf_bytes),
            download_name=f'saskaita_{invoice.invoice_no}.pdf',
            as_attachment=True,
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"PDF generation error: {e}")
        return "Error generating PDF", 500
    
@app.route('/quit')
def quit():
    def shutdown():
        import time
        time.sleep(2)
        os._exit(0)
    
    Thread(target=shutdown).start()
    return '''
    <script>
        // Try to close (works in some cases)
        window.close();
    </script>
    <div style="text-align: center; padding: 50px; font-family: Arial;">
        <h2>Programa uždaroma...</h2>
        <p>Prašome uždarykite šį naršyklės langą rankiniu būdu.</p>
        <p style="color: #666;">Serveris bus išjungtas už 2 sekundžių.</p>
    </div>
    '''