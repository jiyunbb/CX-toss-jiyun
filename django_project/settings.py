from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "F645B5810A118A3C8A2C68C720F31084388B586B549E4667D6000B74BB007D36"
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "apps.core",
]
MIDDLEWARE = []
ROOT_URLCONF = "django_project.urls"
TEMPLATES = []
WSGI_APPLICATION = "django_project.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = False
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
