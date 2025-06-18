# 💱 CurrencyFlow

**CurrencyFlow** est une application de bureau simple et élégante, écrite en Python avec PyQt6, permettant de convertir des devises (monnaies FIAT et cryptomonnaies) en temps réel. L’application utilise une API publique pour récupérer les taux de change et stocke localement les préférences et l’historique en JSON.

---

## 📸 Aperçu

- Interface ergonomique (PyQt6) avec champs intuitifs :
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
|-----------------|--------------------|
| Langage         | Python 3.11+       |
| UI              | PyQt6              |
| API             | [exchangerate.host](https://exchangerate.host)|
| Stockage local  | JSON (`data/`)     |
| Gestion API     | `requests`         |

---

### 🔐 Gestion de la clé API

Si l'API choisie nécessite une clé, **ne la mettez jamais en clair dans le code**. Voici comment la protéger :

1. Créez un fichier `.env` (non versionné) à la racine du projet :
   ```ini
   API_KEY=ta_clé_secrète_ici
   ```
2. Ajoutez `.env` au fichier `.gitignore`
3. Utilisez `python-dotenv` pour charger la clé :
   ```bash
   pip install python-dotenv
   ```
4. Dans votre code Python :
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   API_KEY = os.getenv("API_KEY")
   ```

Ainsi, votre clé est utilisée sans être exposée publiquement.

---

## 📂 Structure du projet

```
CurrencyFlow/
├── main.py
├── ui/
│   └── main_window.py
├── services/
│   ├── api_handler.py
│   └── storage.py
├── data/
│   └── history.json
├── assets/
│   └── icons/
├── .env
├── .gitignore
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

---

## 📦 Dépendances

```txt
PyQt6
requests
python-dotenv
```

(Installées via `requirements.txt`)

---

## ▶️ Lancer l'application

```bash
python main.py
```

---

## ✍️ À venir

- ⬛ Rafraîchissement automatique des taux
- ⬛ Export CSV ou PDF de l’historique
- ⬛ Intégration d'un widget graphique pour les fluctuations

---
