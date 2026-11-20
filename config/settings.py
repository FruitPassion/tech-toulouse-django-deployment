"""
Réglages du projet. Tout ce qui change d'un endroit à l'autre (votre machine, la
plateforme Tech-Toulouse) se lit dans l'environnement : ce fichier n'a rien à modifier
pour être déployé.
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def required(name):
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"La variable d'environnement {name} est obligatoire (voir le README).")
    return value


# 1. La clé qui signe les sessions : fournie par la plateforme, jamais dans le dépôt.
SECRET_KEY = required("SECRET_KEY")

# 2. Désactivé partout sauf si vous écrivez DEBUG=1 sur votre machine.
DEBUG = os.environ.get("DEBUG", "0") == "1"

# 3. L'adresse du site. Plusieurs valeurs : séparées par des virgules.
ALLOWED_HOSTS = [host for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host]

# 4. Sans elle, tout formulaire POST (celui de /admin/ compris) répond 403 derrière HTTPS.
CSRF_TRUSTED_ORIGINS = [origin for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if origin]

# 5. La base : PostgreSQL ou MariaDB, fournie par la plateforme. Pas de repli sur SQLite :
# le code est en lecture seule et remplacé à chaque déploiement, un fichier .sqlite3 n'y survivrait pas.
DATABASES = {"default": dj_database_url.parse(required("DATABASE_URL"), conn_max_age=60)}

# Traefik termine le HTTPS et transmet le protocole d'origine.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Sert les fichiers statiques depuis STATIC_ROOT : aucun serveur de fichiers n'est devant l'application.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# `collectstatic` y rassemble les fichiers statiques de toutes les applications, pendant le build.
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# Les fichiers envoyés par vos visiteurs : le seul dossier accessible en écriture sur la plateforme.
MEDIA_ROOT = Path(os.environ.get("APP_STORAGE_PATH", BASE_DIR / "media"))
MEDIA_URL = "media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
