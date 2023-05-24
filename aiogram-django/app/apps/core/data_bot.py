from typing import Final

from app.apps.core.models import TGBot
from asgiref.sync import sync_to_async

class CoreDataBot:
    @staticmethod
    def get_bots_from_db():
        return list(TGBot.objects.all().values('bot_on', 'id', 'bot_username'))
        # return list(TGBot.objects.all().values_list('id', 'bot_username', flat=True))

    @staticmethod
    @sync_to_async
    def async_get_bots_from_db():
        return list(TGBot.objects.all().values('bot_on', 'id', 'bot_username'))
        # return list(TGBot.objects.all().values_list('id', 'bot_username', flat=True))

CORE_DATA_BOT: Final[CoreDataBot] = CoreDataBot()
