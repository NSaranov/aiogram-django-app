# Generated by Django 4.1.3 on 2022-12-14 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0033_jrparenttask_issuetype_name_child_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jrparenttask",
            name="parent_key",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Parent Key"
            ),
        ),
        migrations.AlterField(
            model_name="jrtask",
            name="text",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Text"
            ),
        ),
    ]
