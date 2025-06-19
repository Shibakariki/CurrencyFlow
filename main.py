import os
import sys
import json
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QIcon

# === CONFIGURATION ===
load_dotenv()

API_URL = "https://api.exchangerate.host"
API_KEY = os.getenv("API_KEY")
HISTORY_FILE = "data/history.json"

from services.api_handler import APIHandler
from services.storage import Storage
from ui.main_window import MainWindow

def main():
    storage = Storage()
    api_handler = APIHandler(API_URL, API_KEY, storage)
    window = MainWindow(api_handler, storage)
    
    return window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("CurrencyFlow")
    app.setApplicationVersion("1.3.0")
    
    splash_pix = QPixmap("assets/icons/logo.png")
    screen = app.primaryScreen()
    screen_size = screen.size()
    target_width = screen_size.width() // 5  # 1/4 of screen width
    target_height = screen_size.height() // 5  # 1/4 of screen height
    splash_pix = splash_pix.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.show()

    # Simuler chargement pendant 1 seconde
    QTimer.singleShot(1000, splash.close)

    window = main()
    window.setWindowTitle("CurrencyFlow")
    window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
    
    # Center window on screen
    screen_geometry = app.primaryScreen().geometry()
    x = screen_geometry.width() // 2 - window.width() // 4
    y = (screen_geometry.height() - window.height()) // 2
    window.move(x, y)
    
    # Set maximum width and height
    window.setMaximumWidth(screen_geometry.width() // 2)
    window.setMaximumHeight(screen_geometry.height() // 2)
    
    window.show()

    sys.exit(app.exec())