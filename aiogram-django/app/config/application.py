"""
For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
from starlette.datastructures import CommaSeparatedStrings
from pathlib import Path

from app.config import env

# Application definition
INSTALLED_APPS: list[str] = [
    "app.apps.core",
    'app.apps.jira',

]

ALLOWED_HOSTS = list(env("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=[
    '10.0.21.164',
    '10.0.18.243',
    'srvtst_alert_statist.sdvor.local',
    'srvtst_alert_statist.sdvor.com',
    'srvtst_alert_statist.sdvor.local:8080',
    '*',
    '*:*',
]))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = env("LANGUAGE_CODE", cast=str, default="en-us")

TIME_ZONE = env("TIME_ZONE", cast=str, default="UTC")

USE_I18N = env("USE_I18N", cast=bool, default=True)

USE_TZ = env("USE_TZ", cast=bool, default=True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
