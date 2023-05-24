# from admin_extra_buttons.mixins import ExtraButtonsMixin, confirm_action
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action
from django.urls import path
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpResponseRedirect, HttpResponse
from import_export.admin import ImportExportModelAdmin

from app.apps.jira.models import JRUser, JRTask, JRParentTask, JRTemplateCreateTask
from app.apps.core.models import TGMessage, TGRawMessage, TGBot, TGChat, TGLabel
from app.apps.core.models import TGTemplateParseMsg, TGInlineKeyboardButton

from app.apps.jira.service import Service


# import app.delivery.bot.__main__ as polling
# import logging


@admin.register(JRUser)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[JRUser]):
    list_display = ('atlassian_token', 'atlassian_email', 'base_url')


@admin.register(JRTask)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[JRTask]):
    list_display = ('id', 'key', 'project_key', 'parent_key', 'summary', 'text', 'link', 'issuetype_name')
    search_fields = ('summary', 'text', 'link')


@admin.register(JRParentTask)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[JRParentTask]):
    list_display = ('id', 'key', 'project_key', 'parent_key', 'issuetype_name', 'issuetype_name_child')
    search_fields = ('key', 'parent_key')
    list_filter = ('project_key',)


@admin.register(JRTemplateCreateTask)
class CoreAdmin(ExtraButtonsMixin, ImportExportModelAdmin, ModelAdmin[JRTemplateCreateTask]):
    list_display = ('id', 'id_parent_task', 'id_label', 'description')
    search_fields = ('description',)
    list_filter = ('rest_func_url', 'id_label', 'id_parent_task')

    @button(html_attrs={'style': 'background-color:#66FF00;color:black;', 'label': 'hi'})
    def create_issue(self, request):
        def _action(request):
            Issue = Service()
            return Issue.get_summary_descr_txt()

        return confirm_action(self, request, _action, "Create Issue TMS",
                              "Send Req To Jira: Create Issue", )


@admin.register(TGBot)
class CoreAdminBot(ExtraButtonsMixin, ImportExportModelAdmin, ModelAdmin[TGBot]):
    list_display = ('bot_on', 'admin', 'bot_username', 'it_department_owner', 'id',)
    list_filter = ('bot_username',)

    # @button(html_attrs={'style': 'background-color:#66FF00;color:black;', 'label': 'hi'},
    #         )
    # def start_polling_bots(self, request):
    #     def _action(request):
    #         return polling.start_polling()
    #
    #     return confirm_action(self, request, _action, "Start polling active Bots",
    #                           "Successfully executed", )
    #
    # @button(html_attrs={'style': 'background-color:#FFFF00;color:black;'},
    #         )
    # def stop_polling_bots(self, request):
    #     def _action(request):
    #         return polling.stop_polling()
    #
    #     return confirm_action(self, request, _action, "Stop polling all Bots",
    #                           "Successfully executed", )


@admin.register(TGChat)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[TGChat]):
    list_display = ('chat_title', 'id_bot', 'chat_type', 'id',)
    list_filter = ('chat_title', 'chat_type')


@admin.register(TGLabel)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[TGChat]):
    list_display = ('id', 'label')


@admin.register(TGRawMessage)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[TGRawMessage]):
    list_display = ('raw_message', 'chat_name', 'username', 'id')  # 'date_time', 'username', 'chat_id',
    list_filter = ('chat_name', 'username')
    search_fields = ('raw_message',)
    date_hierarchy = 'date_time'


@admin.register(TGMessage)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[TGMessage]):
    list_display = ('id', 'id_template', 'message', 'label', 'chat_name', 'value_float',
                    'value_str')  # 'date_time', 'username', 'chat_id',
    list_filter = ('label', 'chat_name')
    search_fields = ('message', 'label')
    date_hierarchy = 'date_time'


@admin.register(TGTemplateParseMsg)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[TGTemplateParseMsg]):
    list_display = ('id', 'template_on', 'description', 'priority', 'condition_type', 'regex',
                    'replace', 'value_regex', 'value_eq', 'id_chat', 'id_label')
    list_filter = ('id_label', 'id_chat', 'template_on')
    search_fields = ('description', 'condition_type')


@admin.register(TGInlineKeyboardButton)
class CoreAdmin(ImportExportModelAdmin, ModelAdmin[TGInlineKeyboardButton]):
    list_display = ('id', 'admin', 'id_bot', 'id_chat', 'button_text', 'callback_data', 'labels')
    list_filter = ('id_bot', 'id_chat')
    search_fields = ('button_text', 'callback_data')
