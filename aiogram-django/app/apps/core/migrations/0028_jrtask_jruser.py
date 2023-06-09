# Generated by Django 4.1.3 on 2022-12-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0027_tgbot_admin_tginlinekeyboardbutton_admin"),
    ]

    operations = [
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
                    models.CharField(max_length=100, null=True, verbose_name="Text"),
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
                "db_table": "jr_task",
            },
        ),
        migrations.CreateModel(
            name="JRUser",
            fields=[
                (
                    "token",
                    models.BigIntegerField(
                        primary_key=True, serialize=False, verbose_name="App Token"
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=64, null=True, verbose_name="Username"),
                ),
            ],
            options={
                "db_table": "jr_user",
            },
        ),
    ]
