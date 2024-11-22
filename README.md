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
uv pip install -e .
```

5. Créez un fichier `.env` à la racine du projet :
```env
SLACK_BOT_TOKEN=xoxb-votre-token-slack
```

## Configuration Slack

1. Créez une App Slack à [https://api.slack.com/apps](https://api.slack.com/apps)
2. Activez les permissions `chat:write` et `files:write`
3. Installez l'app dans votre workspace
4. Copiez le Bot User OAuth Token dans votre fichier `.env`
5. Invitez le bot dans le canal cible : `/invite @votre-bot`

## Utilisation

Pour exécuter le bot :
```bash
python slack_poster.py
```

## Structure du projet

```
appety-bot/
├── .venv/                 # Environnement virtuel uv
├── facebook_scraper.py    # Scraping de la page Facebook
├── slack_poster.py        # Envoi du menu sur Slack
├── pyproject.toml        # Configuration du projet et dépendances
├── .env                   # Configuration (tokens)
└── README.md
```

## Dépendances

Les dépendances sont gérées dans le fichier `pyproject.toml` :
- seleniumbase : Scraping web
- slack-sdk : Intégration Slack
- python-dotenv : Gestion des variables d'environnement

## Développement

Pour installer en mode développement :
```bash
uv pip install -e .
```

Pour ajouter une nouvelle dépendance :
1. Ajoutez-la dans `pyproject.toml`
2. Puis exécutez :
```bash
uv pip install -e .
```

## Note

Le script utilise SeleniumBase qui nécessite un navigateur Chrome. Il sera installé automatiquement lors de la première exécution.
