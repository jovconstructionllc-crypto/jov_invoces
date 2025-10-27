from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from models import db, Client, Invoice, InvoiceLine
from forms import ClientForm, InvoiceForm
from datetime import datetime
import os, io, base64
from flask import render_template_string
# PDF libraries (WeasyPrint preferred, fallback to pdfkit)
try:
    from weasyprint import HTML
    WEASY = True
except Exception:
    WEASY = False
try:
    import pdfkit
    PDFKIT = True
except Exception:
    PDFKIT = False

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','change-me-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_odoo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Clients
@app.route('/clients')
def clients():
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)

@app.route('/clients/create', methods=['GET','POST'])
def create_client():
    form = ClientForm()
    if form.validate_on_submit():
        c = Client(name=form.name.data, email=form.email.data, phone=form.phone.data, address=form.address.data)
        db.session.add(c)
        db.session.commit()
        flash('Client created', 'success')
        return redirect(url_for('clients'))
    return render_template('create_client.html', form=form)

# Invoices
@app.route('/invoices')
def invoices():
    invs = Invoice.query.order_by(Invoice.date.desc()).all()
    return render_template('invoices.html', invoices=invs)

@app.route('/invoices/create', methods=['GET','POST'])
def create_invoice():
    form = InvoiceForm()
    if request.method == 'POST':
        num = request.form.get('number') or f"INV-{int(datetime.utcnow().timestamp())}"
        client_id = int(request.form.get('client_id'))
        date = request.form.get('date') or None
        due_date = request.form.get('due_date') or None
        notes = request.form.get('notes')
        doc_type = request.form.get('doc_type','invoice')  # invoice or estimate
        invoice = Invoice(number=num, notes=notes, client_id=client_id, doc_type=doc_type)
        if date:
            invoice.date = datetime.fromisoformat(date).date()
        if due_date:
            invoice.due_date = datetime.fromisoformat(due_date).date()
        descs = request.form.getlist('desc[]')
        qtys = request.form.getlist('qty[]')
        prices = request.form.getlist('price[]')
        for d,q,p in zip(descs, qtys, prices):
            if not d:
                continue
            try:
                qf = float(q)
            except:
                qf = 1
            try:
                pf = float(p)
            except:
                pf = 0.0
            line = InvoiceLine(description=d, qty=qf, unit_price=pf)
            invoice.lines.append(line)
        db.session.add(invoice)
        db.session.commit()
        flash('Document created', 'success')
        return redirect(url_for('invoices'))
    clients = Client.query.all()
    return render_template('create_invoice.html', form=form, clients=clients)

@app.route('/invoices/<int:invoice_id>')
def invoice_detail(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice_detail.html', invoice=inv)

def image_to_data_uri(path):
    if not path or not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        data = f.read()
    mime = 'image/png' if path.lower().endswith('.png') else 'image/jpeg'
    return 'data:%s;base64,%s' % (mime, base64.b64encode(data).decode('utf-8'))

@app.route('/invoices/<int:invoice_id>/pdf')
def invoice_pdf(invoice_id):
    inv = Invoice.query.get_or_404(invoice_id)
    company_name = "JOV Construction LLC"
    company_address = "2237 Dellridge Ave, Saint Paul, MN 55119"
    company_phone = "651-353-6948"
    company_legal = ""
    company_contact = "jovconstruction@gmail.com"
    logo_path = os.path.join(app.root_path, 'static', 'logo.png')
    logo_data = image_to_data_uri(logo_path)
    html_out = render_template('invoice_pdf.html',
                              invoice=inv,
                              company_name=company_name,
                              company_address=company_address,
                              company_phone=company_phone,
                              company_legal=company_legal,
                              company_contact=company_contact,
                              company_logo=logo_data)
    if WEASY:
        pdf_file = HTML(string=html_out, base_url=request.base_url).write_pdf()
    elif PDFKIT:
        pdf_file = pdfkit.from_string(html_out, False)
    else:
        return "PDF generation not available on this deployment. Install WeasyPrint or wkhtmltopdf.", 500
    return send_file(
        io.BytesIO(pdf_file),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Document_{inv.number}.pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
