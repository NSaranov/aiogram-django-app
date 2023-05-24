from typing import Final

from asgiref.sync import sync_to_async

from app.apps.core.models import TGTemplateParseMsg
from django.db.models import F


class CoreDataTemplate:
    @sync_to_async()
    @staticmethod
    def get_templates_from_db(self, chat_id):
        return list(
            TGTemplateParseMsg.objects.filter(id_chat__id=chat_id, template_on=True
                                              ).order_by('priority'
                                                         ).annotate(label=F('id_label__label'
                                                                            )).values('id',
                                                                                      'label',
                                                                                      'regex',
                                                                                      'replace',
                                                                                      'value_regex',
                                                                                      'value_eq',
                                                                                      'priority',
                                                                                      'condition_type'))


CORE_DATA_TEMPLATE: Final[CoreDataTemplate] = CoreDataTemplate()
