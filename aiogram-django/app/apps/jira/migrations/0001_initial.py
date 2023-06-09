# Generated by Django 4.1.3 on 2022-12-14 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0038_delete_jruser"),
    ]

    operations = [
        migrations.CreateModel(
            name="JRParentTask",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        primary_key=True, serialize=False, verbose_name="PTask ID"
                    ),
                ),
                ("key", models.CharField(max_length=64, null=True, verbose_name="Key")),
                (
                    "project_key",
                    models.CharField(
                        max_length=64, null=True, verbose_name="Project Key"
                    ),
                ),
                (
                    "parent_key",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="Parent Key"
                    ),
                ),
                (
                    "issuetype_name",
                    models.CharField(max_length=30, null=True, verbose_name="Issue Type"),
                ),
                (
                    "issuetype_name_child",
                    models.CharField(
                        max_length=30, null=True, verbose_name="Issue Type Child"
                    ),
                ),
            ],
            options={
                "verbose_name": "Parent Task",
                "verbose_name_plural": "Parent Tasks",
                "db_table": "jr_parent_task",
            },
        ),
        migrations.CreateModel(
            name="JRTask",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        primary_key=True, serialize=False, verbose_name="Task ID"
                    ),
                ),
                ("key", models.CharField(max_length=64, null=True, verbose_name="Key")),
                (
                    "project_key",
                    models.CharField(
                        max_length=64, null=True, verbose_name="Project Key"
                    ),
                ),
                (
                    "parent_key",
                    models.CharField(max_length=64, null=True, verbose_name="Parent Key"),
                ),
                (
                    "summary",
                    models.CharField(max_length=100, null=True, verbose_name="Summary"),
                ),
                (
                    "text",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Text"
                    ),
                ),
                (
                    "issuetype_name",
                    models.CharField(max_length=30, null=True, verbose_name="Issue Type"),
                ),
                (
                    "link",
                    models.CharField(max_length=100, null=True, verbose_name="Link"),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
                "db_table": "jr_task",
            },
        ),
        migrations.CreateModel(
            name="JRUser",
            fields=[
                (
                    "atlassian_token",
                    models.CharField(
                        max_length=64,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Access Token",
                    ),
                ),
                (
                    "atlassian_email",
                    models.CharField(max_length=64, null=True, verbose_name="Email"),
                ),
                (
                    "baseUrl",
                    models.CharField(
                        max_length=64, null=True, verbose_name="Atlassian Base Url"
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "db_table": "jr_user",
            },
        ),
        migrations.CreateModel(
            name="JRTemplateCreateTask",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "description",
                    models.CharField(max_length=80, null=True, verbose_name="Descript"),
                ),
                (
                    "rest_func_url",
                    models.CharField(
                        max_length=64, null=True, verbose_name="RestFuncUrl"
                    ),
                ),
                (
                    "request_header",
                    models.TextField(max_length=100, null=True, verbose_name="ReqHeader"),
                ),
                (
                    "request_body",
                    models.TextField(max_length=1000, null=True, verbose_name="ReqBody"),
                ),
                (
                    "id_label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.tglabel",
                        verbose_name="Label",
                    ),
                ),
                (
                    "id_parent_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="jira.jrparenttask",
                        verbose_name="ParentTask",
                    ),
                ),
            ],
            options={
                "verbose_name": "Template Create Task",
                "verbose_name_plural": "Template Create Tasks",
                "db_table": "jr_template_create_task",
            },
        ),
    ]
