import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox
)

SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CAD", "BTC", "ETH"]

class MainWindow(QWidget):
    def __init__(self, api_handler, storage):
        super().__init__()
        self.api_handler = api_handler
        self.storage = storage
        
        self.init_ui()

    def init_ui(self):
        # Démarre l’interface utilisateur
        layout = QVBoxLayout()

        # Source currency
        self.from_currency = QComboBox()
        self.from_currency.addItems(SUPPORTED_CURRENCIES)
        self.from_currency.setCurrentIndex(0)

        # Target currency
        self.to_currency = QComboBox()
        self.to_currency.addItems(SUPPORTED_CURRENCIES)
        self.to_currency.setCurrentIndex(1)

        # Amount input
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Montant à convertir")

        # Result label
        self.result_label = QLabel("Résultat :")

        # Convert button
        self.convert_btn = QPushButton("Convertir")
        self.convert_btn.clicked.connect(self.on_convert_clicked)

        # Layouts
        layout.addWidget(QLabel("De :"))
        layout.addWidget(self.from_currency)
        layout.addWidget(QLabel("À :"))
        layout.addWidget(self.to_currency)
        layout.addWidget(self.amount_input)
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

