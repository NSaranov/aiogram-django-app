# Generated by Django 4.1.3 on 2022-12-14 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0037_delete_jrtask_remove_jrtemplatecreatetask_id_label_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="JRUser",
        ),
    ]
