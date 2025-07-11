from EasyInvoice import app, db
from EasyInvoice.models import Client, Invoice

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)