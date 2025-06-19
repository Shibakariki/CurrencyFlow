import sys
import time

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QFrame
)
from PyQt6.QtGui import QIcon
import requests
from PyQt6.QtWidgets import QScrollArea

class QHistory(QFrame):
    def __init__(self, history, line_clicked_callback=None):
        super().__init__()
        self.line_clicked_callback = line_clicked_callback
        
        # Create scroll area
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        
        # Create widget to contain the layout
        self.content = QWidget()
        self.scroll.setWidget(self.content)
        
        # Main layout for the frame
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)
        
        self._init_layout(history)

    def _init_layout(self, history):
        layout = QVBoxLayout(self.content)
        self.history_label = QLabel("Historique des conversions :")
        self.history_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.history_label)
        
        for idx, item in enumerate(history):
            timestamp = item.get('timestamp', '')
            date_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(timestamp))
            line_btn = QPushButton(f"{date_time} | {item.get('amount', '')} {item.get('from', '')} → {item.get('result', '')} {item.get('to', '')}")
            line_btn.setStyleSheet("text-align: center; padding: 2px;")
            if self.line_clicked_callback:
                line_btn.clicked.connect(lambda checked, i=item: self.line_clicked_callback(i))
            layout.addWidget(line_btn)

            buttons_layout = QHBoxLayout()
            
            copy_result_btn = QPushButton("Copier le résultat")
            copy_result_btn.setToolTip(str(item.get('result', '')))
            copy_result_btn.clicked.connect(lambda _, result=item.get('result', ''): QApplication.clipboard().setText(str(result)))
            buttons_layout.addWidget(copy_result_btn)
            
            copy_rate_btn = QPushButton("Copier le taux de change")
            copy_rate_btn.setToolTip(str(item.get('rate', '')))
            copy_rate_btn.clicked.connect(lambda _, rate=item.get('rate', ''): QApplication.clipboard().setText(str(rate)))
            buttons_layout.addWidget(copy_rate_btn)
            
            layout.addLayout(buttons_layout)

            if idx < len(history) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                layout.addWidget(line)

    def update_history(self, history):
        self._init_layout(history)
        self.adjustSize()

class MainWindow(QWidget):
    def __init__(self, api_handler, storage):
        super().__init__()
        self.setWindowIcon(QIcon("assets/icons/icon.ico"))
        self.api_handler = api_handler
        self.storage = storage
        self.supported_currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"]
        self.supported_currencies = self.api_handler.fetch_supported_currencies() # Commenté cette ligne si vous voulez utiliser la liste par défaut et éviter les appels API
        if not self.supported_currencies:
            QMessageBox.critical(self, "Erreur", "Impossible de récupérer les devises supportées.")
            sys.exit(1)
        
        self.init_ui()

    def init_ui(self):
        # Démarre l’interface utilisateur
        layout = QVBoxLayout()

        # Create horizontal layout for amount and source currency
        amount_layout = QHBoxLayout()

        # Amount input
        self.amount_input = QLineEdit()
        self.amount_input.setMaximumWidth(self.width() // 2)
        self.amount_input.setPlaceholderText("Montant à convertir")

        # Source currency
        self.from_currency = QComboBox()
        self.from_currency.setMaximumWidth(self.width() // 5)
        self.from_currency.addItems(self.supported_currencies)
        self.from_currency.setCurrentText("USD")

        # Label between source and target currencies
        self.switch_btn = QPushButton("🔄")
        self.switch_btn.setMaximumWidth(40)
        self.switch_btn.clicked.connect(self.on_switch_currencies)

        # Target currency
        self.to_currency = QComboBox()
        self.to_currency.setMaximumWidth(self.width() // 5)
        self.to_currency.addItems(self.supported_currencies)
        self.to_currency.setCurrentText("EUR")

        # Add widgets to horizontal layout
        amount_layout.addWidget(self.amount_input)
        amount_layout.addWidget(self.from_currency)
        amount_layout.addWidget(self.switch_btn)
        amount_layout.addWidget(self.to_currency)

        # Add amount layout layout to main layout
        layout.addLayout(amount_layout)        

        convert_history_layout = QHBoxLayout()

        # Convert history button
        self.history_btn = QPushButton("Historique")
        self.history_btn.setMaximumWidth(100)
        self.history_btn.clicked.connect(self.on_history_clicked)

        # Convert button
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.on_convert_clicked)

        convert_history_layout.addWidget(self.convert_btn)
        convert_history_layout.addWidget(self.history_btn)

        # Add convert history layout to main layout
        layout.addLayout(convert_history_layout)

        # Add a table to display the conversion history
        self.history = QHistory(self.storage.load_history(), self.on_history_line_clicked)
        self.history.setVisible(False)
        layout.addWidget(self.history)

        self.setLayout(layout)

    def refresh_history(self):
        # Supprime l'ancien widget et en crée un nouveau avec les données à jour
        layout = self.layout()
        layout.removeWidget(self.history)
        self.history.deleteLater()
        self.history = QHistory(self.storage.load_history(), self.on_history_line_clicked)
        self.history.setVisible(True)
        layout.addWidget(self.history)
        self.adjustSize()

    def on_convert_clicked(self):
        from_curr = self.from_currency.currentText()
        to_curr = self.to_currency.currentText()
        amount = self.amount_input.text()
        try:
            amount = float(amount)
            rate, result = self.api_handler.convert_currency(amount, from_curr, to_curr)
            result_dialog = QDialog(self)
            result_dialog.setWindowTitle("Résultat de la conversion")
            
            dialog_layout = QVBoxLayout()
            
            result_text = f"{amount} {from_curr} → {result} {to_curr}\nTaux de change : {rate}"
            result_label = QLabel(result_text)
            dialog_layout.addWidget(result_label)
            
            copy_result_button = QPushButton("Copier le résultat")
            copy_result_button.setToolTip(str(result))
            copy_result_button.clicked.connect(lambda: QApplication.clipboard().setText(str(result)))
            dialog_layout.addWidget(copy_result_button)
            
            copy_rate_button = QPushButton("Copier le taux de change")
            copy_rate_button.setToolTip(str(rate))
            copy_rate_button.clicked.connect(lambda: QApplication.clipboard().setText(str(rate)))
            dialog_layout.addWidget(copy_rate_button)            
            
            result_dialog.setLayout(dialog_layout)
            result_dialog.exec()
            # self.result_label.setText("Dernière conversion effectuée avec succès")
            self.storage.save_history({
                "timestamp": int(time.time()),
                "from": from_curr,
                "to": to_curr,
                "rate": rate,
                "amount": amount,
                "result": result
            })
            self.history.update_history(self.storage.load_history())
            self.history.setVisible(True)
            self.adjustSize()
        except ValueError as ve:
            self.amount_input.clear()
            self.amount_input.setFocus()
            QMessageBox.critical(
                self,
                "Erreur",
                str(ve)
            )
        except requests.exceptions.RequestException as re:
            self.amount_input.clear()
            self.amount_input.setFocus()
            QMessageBox.critical(
                self,
                "Erreur de connexion",
                f"Impossible de se connecter à l'API : {str(re)}"
            )
        except Exception as e:
            self.amount_input.clear()
            self.amount_input.setFocus()
            QMessageBox.critical(
                self,
                "Erreur",
                f"Une erreur s'est produite lors de la conversion : {str(e)}"
            )

    def on_switch_currencies(self):
        # Inverse les devises source et cible
        from_curr = self.from_currency.currentText()
        to_curr = self.to_currency.currentText()
        self.from_currency.setCurrentText(to_curr)
        self.to_currency.setCurrentText(from_curr)

    def on_history_clicked(self):       
        history_visible_state = self.history.isVisible()        
        self.history.setVisible(not history_visible_state)
        self.adjustSize()

    def on_history_line_clicked(self, item):
        from_curr = item.get('from', '')
        to_curr = item.get('to', '')
        amount = item.get('amount', '')
        
        self.from_currency.setCurrentText(from_curr)
        self.to_currency.setCurrentText(to_curr)
        self.amount_input.setText(str(amount))


