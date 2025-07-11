import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    documents_dir = os.path.join(os.path.expanduser("~"), "Documents", "EasyInvoice")
    os.makedirs(documents_dir, exist_ok=True)

    DB_PATH = os.path.join(documents_dir, "saskaitos.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"