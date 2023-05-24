import os

import dj_database_url

from app.config import env
#
# DATABASE_URL = env("DATABASE_URL", cast=str, default="sqlite:///db.sqlite3")
#                                             # default={'ENGINE': 'django.db.backends.sqlite3',
#                                             #          'NAME': os.path.join(os.path.dirname(__file__),'db.sqlite3.')})
#                                             # default="sqlite:///db.sqlite3"
# CONN_MAX_AGE = env("CONN_MAX_AGE", cast=int, default=600)
#
# # DATABASES = {
# #     "default": dj_database_url.parse(DATABASE_URL, conn_max_age=CONN_MAX_AGE),
# # }


