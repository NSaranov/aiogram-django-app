from typing import Final

from asgiref.sync import sync_to_async

from app.apps.core.models import TGInlineKeyboardButton, TGBot
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from django.db.models import Q

class CoreKeybordExport:
    @sync_to_async()
    @staticmethod
    def get_inline_buttons_from_db(self, chat_name: str, bot_username: str):
        # print('chat_name=', chat_name, 'bot_username=', bot_username)
        bot_admin = TGBot.objects.filter(bot_username=bot_username,admin=True).values('admin')
        # print(bot_admin)
        if bot_admin:
            result_query = TGInlineKeyboardButton.objects.filter(Q(admin=True) | Q(id_bot__bot_username=bot_username),
                                                                 ).values('button_text',
                                                                          'callback_data',
                                                                          'labels__label',
                                                                          'id_chat_id')
        else:
            result_query = TGInlineKeyboardButton.objects.filter(id_chat__id=chat_name,
                                                                 id_bot__bot_username=bot_username
                                                                 ).values('button_text',
                                                                          'callback_data',
                                                                          'labels__label',
                                                                          'id_chat_id')
        # print(result_query)
        keyboard = []
        for row in result_query:
            callback_data = f"{row['callback_data']}:" \
                            f"{row['labels__label']}:" \
                            f"{str(chat_name)}" #:" \
                            # f"{str(row['button_text'])}"
            obj = InlineKeyboardButton(text=row['button_text'],
                                       callback_data=callback_data.encode('utf-8'))
            print(callback_data)
            keyboard.append(obj)
        cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel:close")
        choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[keyboard, [cancel_button]])
        return choice


KEYBOARD_EXPORT: Final[CoreKeybordExport] = CoreKeybordExport()
