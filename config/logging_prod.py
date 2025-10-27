import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    # --------- Formatters ---------
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },

    # --------- Handlers ---------
    "handlers": {
        # 📄 Logt alles vanaf INFO naar bestand
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "django_prod.log"),
            "formatter": "verbose",
        },

        # 📨 Stuurt e-mail naar ADMINS bij fouten (500’s, etc.)
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,  # HTML-versie van foutmail
        },
    },

    # --------- Loggers ---------
    "root": {
        "handlers": ["file"],
        "level": "INFO",
    },

    "loggers": {
        # Algemene Django-logging
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        # HTTP request fouten (zoals 500 errors)
        "django.request": {
            "handlers": ["file", "mail_admins"],  # Mail en file log
            "level": "ERROR",
            "propagate": False,
        },
        # Onverwachte security-gerelateerde fouten
        "django.security": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

