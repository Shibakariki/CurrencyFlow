# 💱 CurrencyFlow

**CurrencyFlow** est une application de bureau simple et élégante, écrite en Python avec PyQt6, permettant de convertir des devises (monnaies FIAT et cryptomonnaies) en temps réel. L’application utilise une API publique pour récupérer les taux de change et stocke localement les préférences et l’historique en JSON.

---

## 📸 Aperçu

> Interface ergonomique (PyQt6) avec champs intuitifs :
- Sélection des devises (source et cible)
- Saisie du montant à convertir
- Résultat instantané
- Historique des conversions (stocké localement)

---

## 🚀 Fonctionnalités principales

- ✅ Conversion en temps réel des devises FIAT et crypto les plus populaires
- ✅ Interface moderne avec PyQt6
- ✅ Stockage local (JSON) des préférences et de l’historique
- ✅ Détection automatique des taux de change via une API publique
- ✅ Mode hors-ligne partiel avec les derniers taux sauvegardés

---

## 🛠️ Technologies utilisées

| Composant       | Technologie        |
|----------------|--------------------|
| Langage         | Python 3.10+       |
| UI              | PyQt6              |
| API             | `exchangerate.host` *(ou autre si besoin)* |
| Stockage local  | JSON (`data/`)     |
| Gestion API     | `requests`         |

---

## 📂 Structure du projet

```
CurrencyFlow/
├── main.py
├── ui/
│ └── main_window.py
├── services/
│ ├── api_handler.py
│ └── storage.py
├── data/
│ └── history.json
├── assets/
│ └── icons/
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/CurrencyFlow.git
cd CurrencyFlow
```

### 2. Créer un environnement virtuel
```bash 
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```


### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### ▶️ Lancer l'application

```bash
python main.py
```

### ✍️ À venir
[] Sélection de thèmes (sombre/clair)
[] Rafraîchissement automatique des taux
[] Intégration d'un widget graphique pour les fluctuations
