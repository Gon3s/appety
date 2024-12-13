# Appety Menu Scraper & Slack Bot

Un bot qui récupère le menu du jour depuis la page Facebook d'Appety et le poste automatiquement sur Slack.

## Prérequis

- Python 3.8+
- uv 0.1.0+
- Un bot Slack avec les permissions suivantes :
  - `chat:write`
  - `files:write`

## Installation

1. Clonez le repository :
```bash
git clone https://github.com/Gon3s/appety
cd appety-bot
```

2. Initialisez un projet uv :
```bash
uv venv
```

3. Activez l'environnement virtuel :
```bash
# Windows
.venv/Scripts/activate

# Linux/MacOS
source .venv/bin/activate
```

4. Installez les dépendances avec uv :
```bash
uv pip install -r requirements.txt
```

5. Créez un fichier `.env` à la racine du projet :
```env
SLACK_BOT_TOKEN=xoxb-votre-token-slack
```

## Configuration Slack

1. Créez une App Slack à [https://api.slack.com/apps](https://api.slack.com/apps)
2. Activez les permissions `chat:write` et `files:write`
3. Installez l'app dans votre workspace
4. Récupérez le Bot User OAuth Token (`SLACK_BOT_TOKEN`)
5. Invitez le bot dans le canal cible : `/invite @votre-bot`

## Utilisation

```bash
python main.py --channel "#mon-channel" --retries 4 --delay 30 --log-user "@U1234567"
```

Options disponibles :
- `--channel`, `-c` : Canal Slack cible (défaut: #appety)
- `--retries`, `-r` : Nombre de tentatives (défaut: 4)
- `--delay`, `-d` : Délai entre tentatives en minutes (défaut: 30)
- `--log-user`, `-l` : ID utilisateur pour recevoir les logs

Pour trouver votre ID utilisateur :
1. Ouvrez Slack dans un navigateur
2. Cliquez sur votre profil
3. L'ID sera dans l'URL : `https://app.slack.com/client/.../U01234ABCD`
4. Utilisez cet ID avec l'option `--log-user`

## Structure du projet

```
appety-bot/
├── .venv/                 # Environnement virtuel uv
├── facebook_scraper.py    # Scraping de la page Facebook
├── main.py                # Script principal
├── requirements.txt       # Dépendances du projet
├── .env                   # Configuration (tokens)
└── README.md
```

## Dépendances

Les dépendances sont gérées dans le fichier `requirements.txt` :
- beautifulsoup4 : Parse HTML
- seleniumbase : Scraping web
- slack-sdk : Intégration Slack
- python-dotenv : Gestion des variables d'environnement
- requests : Requête HTTP

## Note

Le script utilise SeleniumBase qui nécessite un navigateur Chrome. Il sera installé automatiquement lors de la première exécution.

## Changelog

### 2024-12-2024
- Ajout d'un cache dans une base de données SQLite
- Réorganisation des fichiers dans des dossiers appropriés
- Ajout de commentaires pour la documentation

### 2024-11-27
- Ajout du système de retry (4 tentatives toutes les 30 minutes)
- Ajout du système de logs utilisateur
- Nouvelle option `--log-user` pour recevoir les logs
- Configuration paramétrable (retries, délais)

### 2024-11-25
- Version initiale
- Scraping Facebook
- Post Slack basique
- Configuration via .env
