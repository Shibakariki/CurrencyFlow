import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, api_handler, storage):
        super().__init__()
        self.api_handler = api_handler
        self.storage = storage
        self.supported_currencies = self.api_handler.fetch_supported_currencies()
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
        label = QLabel(" ➡️ ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Target currency
        self.to_currency = QComboBox()
        self.to_currency.setMaximumWidth(self.width() // 5)
        self.to_currency.addItems(self.supported_currencies)
        self.to_currency.setCurrentText("EUR")

        # Add widgets to horizontal layout
        amount_layout.addWidget(self.amount_input)
        amount_layout.addWidget(self.from_currency)
        amount_layout.addWidget(label)
        amount_layout.addWidget(self.to_currency)

        # Add horizontal layout to main layout
        layout.addLayout(amount_layout)        

        # Convert button
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.on_convert_clicked)

        # Result label
        self.result_label = QLabel("Résultat :")

        # Layouts
        # layout.addWidget(self.from_currency)
        # layout.addWidget(self.to_currency)
        # layout.addWidget(self.amount_input)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def on_convert_clicked(self):
        from_curr = self.from_currency.currentText()
        to_curr = self.to_currency.currentText()
        amount = self.amount_input.text()
        try:
            amount = float(amount)
            self.result_label.setText("Résultat : En attente de conversion...")
            self.result_label.setText(f"Conversion de {amount} {from_curr} à {to_curr}...")
            rate, result = self.api_handler.convert_currency(amount, from_curr, to_curr)
            self.result_label.setText(f"Résultat : {str(result)}")
            self.storage.save_history({
                "from": from_curr,
                "to": to_curr,
                "rate": rate,
                "amount": amount,
                "result": result
            })
        except ValueError:
            self.result_label.setText("Erreur : Veuillez entrer un nombre valide")
        except Exception as e:
            self.result_label.setText(f"Erreur : {e}")

