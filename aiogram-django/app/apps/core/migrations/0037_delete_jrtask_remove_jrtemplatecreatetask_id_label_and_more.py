# Generated by Django 4.1.3 on 2022-12-14 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0036_alter_jrtemplatecreatetask_request_body"),
    ]

    operations = [
        migrations.DeleteModel(
            name="JRTask",
        ),
        migrations.RemoveField(
            model_name="jrtemplatecreatetask",
            name="id_label",
        ),
        migrations.RemoveField(
            model_name="jrtemplatecreatetask",
            name="id_parent_task",
        ),
        migrations.DeleteModel(
            name="JRParentTask",
        ),
        migrations.DeleteModel(
            name="JRTemplateCreateTask",
        ),
    ]
