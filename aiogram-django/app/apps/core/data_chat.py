from typing import Final

from asgiref.sync import sync_to_async

from app.apps.core.models import TGChat


class CoreDataChat:
    @sync_to_async()
    @staticmethod
    def get_chats_from_db(self):
        return list(
            TGChat.objects.all().values_list('id', flat=True))  # 'id_bot', 'id_bot__bot_username'


CORE_DATA_CHAT: Final[CoreDataChat] = CoreDataChat()
