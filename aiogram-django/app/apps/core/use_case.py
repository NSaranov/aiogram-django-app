from datetime import datetime
import io
import re
from typing import Final

import xlwt
from aiogram.types import BufferedInputFile
from asgiref.sync import sync_to_async
from django.db.models import Count
from django.db.models import F
from django.db.models.functions import TruncMonth

from app.apps.core.models import TGUser, TGMessage, TGRawMessage


# The `UseCase` classes are used to separate the business logic from the rest of the code.
# Also, because of this, we can easily use the same business logic in different places.
# For example, in the bot and in the web application.

def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


class CoreUseCase:
    # @staticmethod
    # async def register_bot_user(
    #         user_id: int,
    #         chat_id: int,
    #         username: str | None,
    # ) -> tuple[TGUser, bool]:
    #     return await TGUser.objects.aget_or_create(
    #         id=user_id,
    #         chat_id=chat_id,
    #         username=username,
    #     )

    @staticmethod
    async def add_raw_message_to_db(
            id_tg_msg: int,
            chat_id: int,
            chat_name: str | None,
            username: str | None,
            raw_message: str | None,
            date_time: datetime,
    ) -> {(TGRawMessage, bool)}:
        return await TGRawMessage.objects.aget_or_create(
            id_tg_msg=id_tg_msg,
            chat_id=chat_id,
            chat_name=chat_name,
            username=username,
            raw_message=raw_message,
            date_time=date_time,
        )

    @staticmethod
    async def add_message_to_db(
            id_tg_msg: int,
            chat_id: int,
            chat_name: str | None,
            username: str | None,
            message: str | None,
            label: str | None,
            value_float: float | None,
            value_str: str | None,
            id_template: int,
            date_time: datetime,
    ) -> {(TGMessage, bool)}:
        return await TGMessage.objects.aget_or_create(
            id_tg_msg=id_tg_msg,
            chat_id=chat_id,
            chat_name=chat_name,
            username=username,
            message=message,
            label=label,
            value_float=value_float,
            value_str=value_str,
            id_template=id_template,
            date_time=date_time,
        )

    @sync_to_async()
    @staticmethod
    def get_filtred_message_to_file(self, label: str, prefix_file: str | None):
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Messages', cell_overwrite_ok=True)

        result_query = TGMessage.objects.filter(
            label=label).annotate(
            uniq_month=TruncMonth('date_time'),
            chat=F('chat_name')
        ).values('uniq_month',
                 'chat',
                 'label',
                 'message').order_by('uniq_month'
                                     ).annotate(total=Count('message'))
        # Все месяцы
        months = [dict['uniq_month'] for dict in result_query]
        # Уникальные метки
        uniq_name_month = []
        for month in list(set(months)):
            uniq_name_month.append(month.strftime('%Y-%m'))
        uniq_name_month.sort()

        # Заголовок расширяю месяцами
        columns = ['№', 'chat', 'label', 'message']
        columns.extend(uniq_name_month)

        # Заголовок
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        row_num = 0
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Данные
        # Все сообщения
        messages = [dict['message'] for dict in result_query]
        uniq_messages = []
        # Уникальные сообщения
        for message in list(set(messages)):
            uniq_messages.append(message)
        uniq_messages.sort()

        font_style = xlwt.XFStyle()
        for name_message in uniq_messages:
            row_num += 1
            for row in result_query:
                if row['message'] == name_message:
                    str_1 = str(row['uniq_month'].strftime('%Y-%m'))
                    col_num = columns.index(str_1)
                    ws.write(row_num, col_num, row['total'], font_style)
                    ws.write(row_num, 0, row_num, font_style)
                    ws.write(row_num, 1, row['chat'], font_style)
                    ws.write(row_num, 2, row['label'], font_style)
                    ws.write(row_num, 3, row['message'], font_style)
        export_file = io.BytesIO()
        wb.save(export_file)
        byte_result = export_file.getvalue()
        # file_name = prefix_file + ' - ' + str(datetime.now().strftime('%Y-%m-%d_%H%M%S')) + '.xls'
        file_name = label + ' - ' + str(datetime.now().strftime('%Y-%m-%d_%H%M%S')) + '.xls'
        filename_or_stream = BufferedInputFile(byte_result, filename=file_name)
        return filename_or_stream

    @staticmethod
    async def export_message_to_excel(
    ) -> ( ):
        excel_data = await CoreUseCase.get_all_message()
        return excel_data  # response

    @staticmethod
    async def check_insert_msg_to_db(templates: list[dict[str, int | str | None]],
                                     id_tg_msg: int,
                                     chat_id: int,
                                     chat_name: str,
                                     username: str,
                                     text: str,
                                     date_time: datetime, ) -> ():
        # Все метки шаблонов
        all_label_templates = [dict['label'] for dict in templates]
        uniq_labels = []
        # Уникальные метки
        for label in list(set(all_label_templates)):
            uniq_labels.append(label)
        # Цикл по уникальным меткам шаблона
        TGMessage = None
        is_new = None
        for value in uniq_labels:
            # Цикл по данным шаблонов с фильтром в if
            for template_fields in templates:
                if template_fields['label'] == value:
                    # Нет замены, пропускаем шаблон
                    match_name = re.search(template_fields['regex'], text)
                    result_name = match_name.expand(template_fields['replace']) if match_name else None
                    if result_name is None:
                        continue
                    # Отработал шаблон исключения - пропускаем всю группу шаблонов с одной меткой
                    if template_fields['condition_type'] == 'Ex' and result_name is not None:
                        break
                    # Отработал шаблон замены - добавляем в БД обработанное сообщение c меткой замены
                    if template_fields['condition_type'] == 'In' and result_name is not None:

                        # Определяю значение
                        result_float = 0.0
                        result_str = ''
                        match_value = re.search(template_fields['value_regex'], text)
                        result_raw_value = match_value.expand(template_fields['value_eq']) if match_value else None
                        if is_number(result_raw_value) and result_raw_value is not None:
                            result_float = float(result_raw_value)
                        else:
                            result_str = result_raw_value
                        if result_raw_value is None and template_fields['report_type'] == 'Counter Uniq':
                            result_float = 1.0

                        TGMessage, is_new = await CORE_USE_CASE.add_message_to_db(
                            id_tg_msg=id_tg_msg,
                            chat_id=chat_id,
                            chat_name=chat_name,
                            username=username,
                            message=result_name.strip(),
                            label=template_fields['label'],
                            value_float=result_float,
                            value_str=result_str.strip(),
                            id_template=template_fields['id'],
                            date_time=date_time)
        return TGMessage, is_new

    @staticmethod
    async def create_request_to_jira( text: str,
                                      date_time: datetime, ) -> ():
        pass
        # # Нет замены, пропускаем шаблон
        # match_name = re.search(template_fields['regex'], text)
        # result_name = match_name.expand(template_fields['replace']) if match_name else None
        #     if result_name is None:
        #         continue

def time_str_millisec_to_hms(millis):
    millis = int(float(millis))
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60)) % 24
    return hours, minutes, seconds

# Alternative: use a DI middleware to inject the use case into the handler.
# To provide DI middleware, you need to use a third-party library.
# For example, https://github.com/MaximZayats/aiogram-di
CORE_USE_CASE: Final[CoreUseCase] = CoreUseCase()
