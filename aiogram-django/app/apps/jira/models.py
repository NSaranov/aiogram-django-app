from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from asgiref.sync import sync_to_async
from ..core.models import TGLabel


class JRUser(models.Model):
    atlassian_token = models.CharField(max_length=64, primary_key=True, verbose_name="Access Token")
    atlassian_email = models.CharField(max_length=64, null=True, verbose_name="Email")
    base_url = models.CharField(max_length=64, null=True, verbose_name="Atlassian Base Url")

    objects: models.manager.BaseManager["JRUser"]

    @sync_to_async()
    @staticmethod
    def aget_auth_data(self, email):
        try:
             data = JRUser.objects.values('atlassian_token', 'atlassian_email', 'base_url').get(atlassian_email=email)
        except ObjectDoesNotExist:
            data = None
        return data

    class Meta:
        db_table = "jr_user"
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class JRTask(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name="Task ID")
    key = models.CharField(max_length=64, null=True, verbose_name="Key")
    project_key = models.CharField(max_length=64, null=True, verbose_name="Project Key")
    parent_key = models.CharField(max_length=64, null=True, verbose_name="Parent Key")
    summary = models.CharField(max_length=100, null=True, verbose_name="Summary")
    text = models.CharField(max_length=300, null=True, blank=True, verbose_name="Text")
    issuetype_name = models.CharField(max_length=30, null=True, verbose_name="Issue Type")
    link = models.CharField(max_length=100, null=True, verbose_name="Link")
    label = models.CharField(max_length=50, null=True, verbose_name="Label")
    date_time = models.DateTimeField(null=True, verbose_name="DateTime")

    objects: models.manager.BaseManager["JRTask"]

    class Meta:
        db_table = "jr_task"
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class JRParentTask(models.Model):
    id = models.BigIntegerField(primary_key=True, verbose_name="PTask ID")
    key = models.CharField(max_length=64, null=True, verbose_name="Key")
    project_key = models.CharField(max_length=64, null=True, verbose_name="Project Key")
    parent_key = models.CharField(max_length=64, null=True, blank=True, verbose_name="Parent Key")
    issuetype_name = models.CharField(max_length=30, null=True, verbose_name="Issue Type")
    issuetype_name_child = models.CharField(max_length=30, null=True, verbose_name="Issue Type Child")

    objects: models.manager.BaseManager["JRParentTask"]

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.key

    @sync_to_async()
    @staticmethod
    def aget_parent_task(self, key: str):
        try:
            data = JRParentTask.objects.values('key', 'project_key', 'issuetype_name_child').get(key=key)
        except ObjectDoesNotExist:
            data = None
        return data

    class Meta:
        db_table = "jr_parent_task"
        verbose_name = 'Parent Task'
        verbose_name_plural = 'Parent Tasks'


class JRTemplateCreateTask(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    id_parent_task = models.ForeignKey(JRParentTask, on_delete=models.DO_NOTHING, verbose_name="ParentTask")
    id_label = models.ForeignKey(TGLabel, on_delete=models.DO_NOTHING, verbose_name="Label")
    description = models.CharField(max_length=80, null=True, verbose_name="Descript")
    rest_func_url = models.CharField(max_length=64, null=True, verbose_name="RestFuncUrl")
    request_header = models.TextField(max_length=100, null=True, verbose_name="ReqHeader")
    request_body = models.TextField(max_length=1000, null=True, verbose_name="ReqBody")

    objects: models.manager.BaseManager["JRTemplateCreateTask"]

    @sync_to_async()
    @staticmethod
    def aget_template_task(self, key_parent_task: str):
        try:
            data = JRTemplateCreateTask.objects.values('id_label__label',
                                                       'rest_func_url',
                                                       'request_header',
                                                       'request_body').get(id_parent_task__key=key_parent_task)
        except ObjectDoesNotExist:
            data = None
        return data

    class Meta:
        db_table = "jr_template_create_task"
        verbose_name = 'Template Create Task'
        verbose_name_plural = 'Template Create Tasks'
