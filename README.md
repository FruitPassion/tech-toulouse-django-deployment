# Gabarit Django pour Tech-Toulouse

Un projet Django minimal, prêt à être déployé sur la plateforme Tech-Toulouse (stack **PYP**, Python et PostgreSQL). Il sert de point de départ : copiez-le, renommez ce qui doit l'être, et commencez par `home/`.

| Stack | Branche | Pilote de base |
| --- | --- | --- |
| PYP (PostgreSQL) | `main` | `psycopg[binary]` |
| PYM (MariaDB) | `mariadb` | `mysqlclient` |

Les deux branches ne diffèrent que par une ligne de `requirements.txt`. Les deux pilotes ne se combinent pas dans un même fichier : `mysqlclient` ne se compile que sur une stack MariaDB.

## Déployer

1. Faites-en un dépôt à vous (« Use this template » ou un fork), sur la branche qui correspond à votre stack.
2. Créez un projet Python sur la plateforme avec les réglages suivants :
   - framework : **Django** ;
   - version de Python : **3.12 ou plus** (Django 6 ne tourne pas sur 3.11) ;
   - point d'entrée : `config.wsgi:application`.
3. À chaque déploiement, la plateforme installe `requirements.txt`, joue `manage.py migrate` puis `manage.py collectstatic`, importe le point d'entrée, et seulement ensuite publie le site. Tout est dans l'onglet **Build**.

Le site répond sur la page d'accueil, et `/admin/` charge son CSS : c'est WhiteNoise qui sert les fichiers statiques, aucun serveur de fichiers n'est devant l'application.

## Ce que la plateforme fournit

Cinq réglages sont lus depuis l'environnement dans `config/settings.py`. Vous n'écrivez aucun secret dans le dépôt.

| Variable | Rôle |
| --- | --- |
| `SECRET_KEY` | clé de signature des sessions, générée une fois par la plateforme |
| `DEBUG` | `0` sur la plateforme |
| `DJANGO_ALLOWED_HOSTS` | l'adresse du site, pour `ALLOWED_HOSTS` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://` suivi de cette adresse, pour `CSRF_TRUSTED_ORIGINS` |
| `DATABASE_URL` | la base du projet (PostgreSQL ou MariaDB) |

**SQLite est refusé** : le code est en lecture seule et remplacé à chaque déploiement, un fichier `db.sqlite3` n'y survivrait pas. Le gabarit n'a donc aucun repli sur SQLite et s'arrête avec un message clair si `DATABASE_URL` manque.

Les fichiers que vos visiteurs envoient (`MEDIA_ROOT`) vont sous `APP_STORAGE_PATH`, le seul dossier accessible en écriture.

## Travailler sur votre machine

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY=une-valeur-pour-le-developpement DEBUG=1
export DATABASE_URL=postgresql://utilisateur:motdepasse@localhost:5432/ma_base
python manage.py migrate
python manage.py runserver
```

Une base PostgreSQL locale se lance en une commande :

```bash
docker run --rm -e POSTGRES_PASSWORD=motdepasse -e POSTGRES_USER=utilisateur -e POSTGRES_DB=ma_base -p 5432:5432 postgres:18-alpine
```

## Contenu

- `config/` : les réglages (`settings.py`), les routes, le point d'entrée WSGI ;
- `home/` : une application d'exemple, une vue, un gabarit, un fichier CSS ;
- `requirements.txt` : les dépendances, épinglées. gunicorn n'y figure pas, la plateforme le fournit.
