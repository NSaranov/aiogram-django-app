# Generated by Django 4.1.3 on 2022-11-23 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_tgmessage_id_template_tgmessage_id_tg_msg_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgmessage',
            name='id_tg_msg',
            field=models.BigIntegerField(default=0, verbose_name='ID Telegram Msg'),
        ),
        migrations.AlterField(
            model_name='tgrawmessage',
            name='id_tg_msg',
            field=models.BigIntegerField(default=0, verbose_name='ID Telegram Msg'),
        ),
    ]
