# ManageColis - Application de Gestion de Colis

Application web Django pour la gestion de colis avec suivi en temps réel.

## 📋 Description

ManageColis est une application web permettant aux utilisateurs de:
- Enregistrer des colis avec des informations détaillées
- Suivre l'état de leurs colis en temps réel
- Consulter la liste de tous leurs colis
- Modifier les informations d'un colis
- Supprimer un colis

## 🚀 Fonctionnalités

### Gestion des Utilisateurs
- Inscription avec création automatique d'un code client unique
- Connexion sécurisée
- Affichage du code client dans le profil utilisateur

### Gestion des Colis
- **Création**: Enregistrement de nouveaux colis avec:
  - Description
  - Type (Document, Colis standard, Marchandise commerciale, etc.)
  - Poids
  - Destination (via succursale)
  - Récepteur (via code client)
  - Génération automatique d'un code colis unique (format: COL-XXXX-YYYY)

- **Liste**: Affichage de tous les colis de l'utilisateur connecté avec:
  - Code du colis
  - Récepteur (nom et téléphone)
  - Succursale
  - Heure d'arrivée
  - Poids
  - État (avec badges colorés)

- **Détails**: Affichage complet des informations d'un colis

- **Modification**: Mise à jour des informations d'un colis existant

- **Suppression**: Suppression d'un colis avec confirmation

- **Suivi**: Recherche d'un colis par son code pour consulter son état

## 🛠️ Technologies Utilisées

- **Backend**: Django 5.2
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: jQuery, Bootstrap JS
- **Base de données**: SQLite (par défaut)

## 📁 Structure du Projet

```
PROJET_DJANGO/
├── app/
│   ├── migrations/          # Migrations de la base de données
│   ├── models.py           # Modèles (Client, Succursale, Colis)
│   ├── views.py            # Vues de l'application
│   └── ...
├── gestion_colis/
│   ├── settings.py         # Configuration du projet
│   ├── urls.py             # Configuration des URLs
│   └── ...
├── templates/              # Templates Django
│   ├── base.html           # Template de base
│   ├── authentication-login.html
│   ├── authentication-register.html
│   ├── enregistrer-colis.html
│   ├── lister-colis.html
│   ├── detail-colis.html
│   ├── modifier-colis.html
│   └── suivre-colis.html
├── static/                 # Fichiers statiques (CSS, JS, images)
└── media/                  # Fichiers uploadés (pièces d'identité)
```

## 🗄️ Modèles de Données

### Client
- nom, prénom, postnom
- téléphone
- code (généré automatiquement)
- adresse
- pièce d'identité
- date et lieu de naissance
- user (ForeignKey vers User)

### Succursale
- nom
- ville
- adresse

### Colis
- poids
- type
- description
- destination
- expediteur (ForeignKey vers Client)
- recepteur (ForeignKey vers Client)
- succursale (ForeignKey vers Succursale)
- heure_depart
- heure_arrivee
- code (généré automatiquement)
- etat (traitement, voyage, arrive, annule)
- est_valider

## 📦 Code Colis

Le code colis est généré automatiquement lors de la création avec le format:
**COL-XXXX-YYYY**

- `COL`: Préfixe constant
- `XXXX`: 4 premières lettres du type en majuscules
- `YYYY`: ID du colis avec padding de 4 zéros

**Exemples:**
- Document ID 1 → `COL-DOCU-0001`
- Colis standard ID 5 → `COL-COLI-0005`
- Marchandise commerciale ID 10 → `COL-MARC-0010`

## 🎯 États d'un Colis

- **traitement**: En cours de traitement (badge jaune)
- **voyage**: En transit (badge bleu)
- **arrive**: Arrivé à destination (badge vert)
- **annule**: Annulé (badge rouge)

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes d'installation

1. Cloner le repository:
```bash
git clone <repository-url>
cd PROJET_DJANGO
```

2. Créer un environnement virtuel:
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances:
```bash
pip install django
```

4. Exécuter les migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Créer un superutilisateur (optionnel):
```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement:
```bash
python manage.py runserver
```

7. Accéder à l'application:
```
http://127.0.0.1:8000/
```

## 📝 Utilisation

### Inscription
1. Accéder à la page d'inscription
2. Remplir le formulaire avec vos informations
3. Votre code client sera généré automatiquement et affiché

### Enregistrer un Colis
1. Connectez-vous à votre compte
2. Cliquez sur "Enregistrer un colis"
3. Remplissez les informations du colis
4. Le code colis sera généré automatiquement

### Suivre un Colis
1. Accédez à la page "Suivre un colis"
2. Entrez le code du colis
3. Vous serez redirigé vers les détails du colis

## 🔧 Configuration

### Base de données
Par défaut, le projet utilise SQLite. Pour utiliser PostgreSQL ou MySQL, modifiez la configuration dans `gestion_colis/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'managecolis',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Fichiers Statiques
Les fichiers statiques sont situés dans le dossier `static/`. Pour le déploiement en production, configurez `STATIC_ROOT` et utilisez `collectstatic`.

## 📄 Licence

Ce projet est développé à des fins éducatives.

## 👨‍💻 Auteur

Projet développé dans le cadre d'une formation Django.

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou un pull request.