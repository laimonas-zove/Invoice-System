# EasyInvoice - invoice system

EasyInvoice is a lightweight invoice generation system designed specifically for self-employed individuals (operating under individuali veikla) in Lithuania. It helps you create professional invoices in the Lithuanian language while ensuring compliance with local tax regulations.

## Project Structure

```
Invoice-System/
├── EasyInvoice/
│   ├── static/
│   │   ├── css/
│   │   │   ├── base.css          # CSS styles
│   │   ├── images/
│   │   │   ├── icon.ico          # Application icon
│   │   │   ├── logo_dark.png     # Logo for white background
│   │   │   ├── logo_white.png    # Logo for dark background
│   │   │   ├── logo.png          # Application logo
│   ├── templates/
│   │   ├── clients/
│   │   │   ├── add_new.html      # New client template
│   │   │   ├── clients.html      # Clients template
│   │   │   ├── edit.html         # Edit client template
│   │   ├── invoices/
│   │   │   ├── add_new.html      # New invoice template
│   │   │   ├── edit.html         # Edit client template
│   │   │   ├── invoice.html      # PDF invoice template
│   │   │   ├── invoices.html     # Invoices template
│   │   ├── base_index.html       # Base template
│   │   ├── index.html            # Index template
│   │   ├── provider.html         # Provider template
│   ├── __init__.py               # App factory
│   ├── config.py                 # Configuration
│   ├── forms.py                  # Flask-WTF forms
│   ├── models.py                 # SQLAlchemy models
│   ├── routes.py                 # Flask routes and views
│   ├── utils.py                  # Utility functions
├── output/
│   ├── EasyInvoiceInstaller.exe  # Application installer
├── run.py                        # Main app
├── run.bat                       # Batch file to start
├── requirements.txt              # Python dependencies
├── python-3.13.0-amd64.exe       # Python installer
```

## Run Locally

Clone the repository

```bash
  git clone https://github.com/laimonas-zove/Invoice-System
```

Go to the project directory

```bash
  cd Invoice-System
```

Set Up a Virtual Environment

```bash
  python -m venv .venv
  .venv\Scripts\activate
```

Install Required Dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python run.py
```

This starts the application at: (http://127.0.0.1:5000)

### Optional: Use the Installer

You can also run the application via the Windows installer:

```bash
  EasyInvoice/output/EasyInvoiceInstaller.exe
```

## Authors

- [@Laimonas-Zovė](https://github.com/laimonas-zove)
