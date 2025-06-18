import os
import sys
import json
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

# === CONFIGURATION ===
load_dotenv()

API_URL = "https://api.exchangerate.host/live"
API_KEY = os.getenv("API_KEY")
HISTORY_FILE = "data/history.json"

from services.api_handler import APIHandler
from services.storage import Storage
from ui.main_window import MainWindow

def main():
    api_handler = APIHandler(API_URL, API_KEY)
    storage = Storage()
    window = MainWindow(api_handler, storage)
    return window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("CurrencyFlow")
    app.setApplicationVersion("1.0.0")

    window = main()  # window est bien une instance de MainWindow
    window.setWindowTitle("CurrencyFlow")
    window.setGeometry(100, 100, 400, 200)
    window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
    window.show()

    sys.exit(app.exec())