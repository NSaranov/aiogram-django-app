# Generated by Django 4.1.3 on 2022-11-25 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_tgtemplateparsemsg_id_chat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgtemplateparsemsg',
            name='report_type',
            field=models.CharField(choices=[('Counter Uniq', 'Counter Uniq'), ('Collector Value', 'Collector Value'), ('', '')], default='', max_length=30, verbose_name='Report'),
        ),
    ]
