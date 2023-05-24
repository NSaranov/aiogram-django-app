import json
import logging
import re
import time

from aiogram import Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.methods import SendDocument
from aiogram.types import Message, CallbackQuery

from app.apps.core.data_chat import CORE_DATA_CHAT
from app.apps.core.data_template import CORE_DATA_TEMPLATE
from app.apps.core.keybord.callback import ExportCallback, CancelCallback
from app.apps.core.keybord.export import CoreKeybordExport
from app.apps.core.use_case import CORE_USE_CASE, time_str_millisec_to_hms
from app.apps.jira.service import Service
from .specifications import Chat_alerts

# from app.config.application import INSTALLED_APPS


router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.channel_post(Command(commands=["export"]))
@router.message(Command(commands=["export"]))
async def handle_post_export_command(message: Message, bot: Bot) -> None:
    bot_data = await bot.get_me()
    choice = await CoreKeybordExport.get_inline_buttons_from_db(chat_name=message.chat.id,
                                                                bot_username=bot_data.username)
    # print(choice)
    await message.answer(text='Выберите отчет:', reply_markup=choice)


@router.callback_query(ExportCallback.filter(F.report == 'statictic'))
async def export_statictic(call: CallbackQuery, callback_data: dict) -> None:
    await call.answer(cache_time=6)

    label = callback_data.__getattribute__("label")
    chat_id = callback_data.__getattribute__("chat_id")
    # prefix_file = callback_data.__getattribute__("prefix_file")
    input_file = await CORE_USE_CASE.get_filtred_message_to_file(label=label, prefix_file=None)
    await SendDocument(chat_id=chat_id, document=input_file, caption=label)


@router.callback_query(CancelCallback.filter(F.action == "close"))
async def button_cancel(call: CallbackQuery) -> None:
    await call.message.edit_reply_markup()


@router.message()
async def save_message_to_db(message: Message) -> None:
    # print(message)
    chats_id = await CORE_DATA_CHAT.get_chats_from_db()
    if message.chat.id not in chats_id:
        return
    if message.text is None:
        text = message.caption
    else:
        text = message.text
    _, is_new = await CORE_USE_CASE.add_raw_message_to_db(
        id_tg_msg=message.message_id,
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        username=message.from_user.username,
        raw_message=text,
        date_time=message.date,
    )
    templates = await CORE_DATA_TEMPLATE.get_templates_from_db(chat_id=message.chat.id)
    if templates is not None:
        need_create_task, \
        descr_new_task = await CORE_USE_CASE.check_insert_msg_to_db(templates=templates,
                                                                    id_tg_msg=message.message_id,
                                                                    chat_id=message.chat.id,
                                                                    chat_name=message.chat.title,
                                                                    username=message.from_user.username,
                                                                    text=text,
                                                                    date_time=message.date)

# JIRA
@router.channel_post(Text(contains="[Проведение процедуры QA]"))
async def create_task_to_QAS_1000(channel_post: Message) -> None:
    chats_id = await CORE_DATA_CHAT.get_chats_from_db()
    if channel_post.sender_chat.id not in chats_id:
        return
    if channel_post.text is None or channel_post.text == "":
        text = str(channel_post.caption)
    else:
        text = str(channel_post.text)
    if text is None:
        return
    text = text.replace('"', ' ')
    regex = str(r'(.*\sRequest: )(.*)(\sType: )(.*)(\sDescription: )(.*)(\sOwner: )(.*)(\sReviewer:)(.*)')
    template_replace = str(r'{"numb": "\2", "type": "\4", "descr": "\6","owner":"\8","reviewer":"\10"}')
    match_value = re.search(regex, text)
    result = match_value.expand(template_replace) if match_value else None
    if result is not None:
        data_sap_req = json.loads(result)
        # obj_service = Service()
        try:
            obj_service = await Service.acreate()
        except Exception as ex_create_issue:
            print("Exception Create Issue = ", ex_create_issue)
        newtask_text = await obj_service.get_summary_descr_text(data_sap_req=data_sap_req, date_time=channel_post.date)

        parent_task, \
        new_task_key, \
        link_new_task, \
        label, \
        transition = await obj_service.create_issue_jira_to_QAS_1000(new_task=newtask_text,
                                                                     descr_req=data_sap_req['descr'],
                                                                     reviewer_req=data_sap_req['reviewer'],
                                                                     date_time=channel_post.date,
                                                                     request=data_sap_req['numb'])

        if parent_task is not None:
            text_answer = '<a href="' + link_new_task + '"> Создана новая задача в Jira: ' + new_task_key + '</a>'
            if label is not None:
                text_answer = text_answer + '\n' + '<b>Метка:</b> ' + label
            if transition is not None:
                text_answer = text_answer + '\n' + '<b>Статус:</b> ' + transition.upper()

        else:
            text_answer = 'Новая задача в Jira не создана'

        # От блокировки за спам рассылки в Telegram
        # https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
        time.sleep(2)
        await channel_post.reply(text=text_answer, disable_web_page_preview=True, parse_mode='HTML')


@router.channel_post(Text(contains="[Проверить старые задачи QAS-1000]"))
async def close_task_to_QAS_1000(channel_post: Message) -> None:
    chats_id = await CORE_DATA_CHAT.get_chats_from_db()
    if channel_post.sender_chat.id not in chats_id:
        return
    if channel_post.text is None or channel_post.text == "":
        text = str(channel_post.caption)
    else:
        text = str(channel_post.text)
    if text is None:
        return
    regex = str(r'^(.*\s.*-)(.*)(д.*)$')
    template_replace = str(r'{"days_ago": "\2"}')
    match_value = re.search(regex, text)
    result = match_value.expand(template_replace) if match_value else None
    if result is not None:
        try:
            days_ago = json.loads(result)
            value_day = days_ago.get('days_ago', None)
            if value_day != '':
                value_day = int(value_day)
            else:
                value_day = int(60)
        except Exception as ex_parse_text_msg:
            print("Exception Parse Value Day Find Close Tasks = ", ex_parse_text_msg)
            value_day = int(60)

        obj_service = await Service.acreate()
        tasks = await obj_service.get_tasks_for_close(value_day)
        count_closed_tasks, list_link_closed_tasks = await obj_service.close_tasks(tasks)
        count = 0
        if count_closed_tasks is not None:
            text_answer = '<b>Количество закрытых задач: </b>' + str(count_closed_tasks)
            for task in list_link_closed_tasks:
                count = count + 1
                text_answer = text_answer + '\n' + str(count) + '. <a href="' + task['link'] + '">' + task[
                    'link'] + '</a>'
                text_answer = text_answer + '\n    приоритет: ' + task['priority']
            time.sleep(2)
            await channel_post.reply(text=text_answer, disable_web_page_preview=True, parse_mode='HTML')


@router.channel_post(Text(contains="[Запрос на освобождение]"))
async def close_task_to_QAS_1000(channel_post: Message) -> None:
    chats_id = await CORE_DATA_CHAT.get_chats_from_db()
    if channel_post.sender_chat.id not in chats_id:
        return
    if channel_post.text is None or channel_post.text == "":
        text = str(channel_post.caption)
    else:
        text = str(channel_post.text)
    if text is None:
        return
    text = text.replace('"', ' ')
    regex = str(r'^(.*\s)(Request: )(.*)(.*\sEmail: )(.*)(\s.*){12,}$')
    template_replace = str(r'{"request":"\3","email":"\5"}')
    match_value = re.search(regex, text)
    result = match_value.expand(template_replace) if match_value else None
    if result is not None:
        request = None
        email = None
        try:
            dict_result = json.loads(result)
            request = dict_result.get('request', None)
            email = dict_result.get('email', None)
        except Exception as ex_parse_text_msg:
            print("Exception Parse Value Examption = ", ex_parse_text_msg)
            return

        summary_dict = {
            "summary": "[{}] Запрос на освобождение".format(request)
        }
        obj_service = await Service.acreate()
        task = await obj_service.find_task_exemption(request)
        is_email_empty = False
        is_email_not_correct = False
        if task is None:
            key, \
            link, \
            new, \
            is_email_empty, \
            is_email_not_correct = await obj_service.create_task_exemption(request, email, summary_dict, text)
        else:
            key, link, new = await obj_service.modify_task_exemption(task, email, text)
        if key is not None:
            if new is True:
                text_operation = 'Создана новая задача ' + str(key)
            else:
                text_operation = 'Обновлена задача ' + str(key)
            text_answer = '<a href="' + link + '">' + text_operation + '</a>'
            if is_email_empty == True:
                text_answer = text_answer + '\n<b>Не указан email</b>'
            if is_email_not_correct == True:
                text_answer = text_answer + '\n<b>В Jira нет пользователя с email="' + str(email) + '"</b>'
            time.sleep(2)
            await channel_post.reply(text=text_answer, disable_web_page_preview=True, parse_mode='HTML')


@router.channel_post(Text(contains="[Alerting]"))
async def close_task_to_QAS_1000(channel_post: Message) -> None:
    chats_id = await CORE_DATA_CHAT.get_chats_from_db()
    if channel_post.sender_chat.id not in chats_id:
        return
    if channel_post.text is None or channel_post.text == "":
        text = str(channel_post.caption)
    else:
        text = str(channel_post.text)
    if text is None:
        return
    if channel_post.sender_chat.id in (Chat_alerts['QAS_Notifications'],
                                       Chat_alerts['QAS_Notifications_Channel']) and text is not None:
        text = text.replace('"', ' ')
        regex = str(r'^(.*Alerting\] )(.*)( - )([\S]{,80})(.*\s){1,}(Metrics:\s.*: )(.*)$')
        template_replace = str(r'{"table":"\2","code_place":"\4","time_execute_msec":"\7"}')
        match_value = re.search(regex, text)
        result = match_value.expand(template_replace) if match_value else None
        if result is not None:
            table = None
            code_place = None
            time_exec_msec = None
            try:
                dict_result = json.loads(result)
                table = dict_result.get('table', None)
                code_place = dict_result.get('code_place', None)
                time_exec_msec = dict_result.get('time_execute_msec', None)
            except Exception as ex_parse_text_msg:
                print("Exception Parse Value Alert = ", ex_parse_text_msg)
                return

            summary_dict = {
                "summary": "{} - {}".format(table, code_place)
            }
            hours, minutes, seconds = time_str_millisec_to_hms(time_exec_msec)
            str_time_execute = str("Время выполнения: %dчас %dмин %dсек" % (hours, minutes, seconds))
            comment = str_time_execute + '\n' + text
            obj_service = await Service.acreate()
            task = await obj_service.find_task_alarm(table, code_place)
            if task is None:
                key, link, new = await obj_service.create_task_alarm(table, code_place, summary_dict, comment)
            else:
                key, link, new = await obj_service.modify_task_alarm(task, table, code_place, comment)
            if key is not None:
                if new is True:
                    text_operation = 'Создана новая задача ' + str(key)
                else:
                    text_operation = 'Обновлена задача ' + str(key)
                text_answer = '<a href="' + link + '">' + text_operation + '</a>'
                time.sleep(2)
                await channel_post.reply(text=text_answer, disable_web_page_preview=True, parse_mode='HTML')


@router.channel_post()
async def save_post_to_db(channel_post: Message) -> None:
    # print(channel_post)
    chats_id = await CORE_DATA_CHAT.get_chats_from_db()
    if channel_post.sender_chat.id not in chats_id:
        return
    if channel_post.text is None or channel_post.text == "":
        text = channel_post.caption
    else:
        text = channel_post.text
    if text is None:
        return
    _, is_new = await CORE_USE_CASE.add_raw_message_to_db(
        id_tg_msg=channel_post.message_id,
        chat_id=channel_post.sender_chat.id,
        chat_name=channel_post.sender_chat.title,
        username=channel_post.sender_chat.username,
        raw_message=text,
        date_time=channel_post.date,
    )
    templates = await CORE_DATA_TEMPLATE.get_templates_from_db(chat_id=channel_post.sender_chat.id)
    if templates is None:
        return
    need_create_task, \
    descr_new_task = await CORE_USE_CASE.check_insert_msg_to_db(templates=templates,
                                                                id_tg_msg=channel_post.message_id,
                                                                chat_id=channel_post.sender_chat.id,
                                                                chat_name=channel_post.sender_chat.title,
                                                                username=channel_post.sender_chat.username,
                                                                text=text,
                                                                date_time=channel_post.date)

