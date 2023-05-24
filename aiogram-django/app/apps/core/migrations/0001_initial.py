# Generated by Django 4.1.3 on 2022-11-22 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TGBot',
            fields=[
                ('id', models.CharField(max_length=60, primary_key=True, serialize=False, verbose_name='Bot Token')),
                ('bot_username', models.CharField(max_length=64, null=True, verbose_name='Bot Username')),
                ('it_department_owner', models.CharField(max_length=64, verbose_name='IT Department Owner')),
            ],
            options={
                'verbose_name': 'Bot',
                'verbose_name_plural': 'Bots',
                'db_table': 'tg_bot',
            },
        ),
        migrations.CreateModel(
            name='TGChat',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_title', models.CharField(max_length=64, null=True, verbose_name='Title')),
                ('id_bot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.tgbot', verbose_name='Message Listening Bot')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
                'db_table': 'tg_chat',
            },
        ),
        migrations.CreateModel(
            name='TGMessage',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(verbose_name='Chat ID')),
                ('chat_name', models.CharField(max_length=64, null=True, verbose_name='Chat Name')),
                ('username', models.CharField(max_length=64, null=True, verbose_name='Username')),
                ('message', models.CharField(max_length=128, null=True, verbose_name='Post Processed Message')),
                ('label', models.CharField(max_length=64, null=True, verbose_name='Label Post Processed Msg')),
                ('date_time', models.DateTimeField(null=True, verbose_name='Create Datetime')),
            ],
            options={
                'verbose_name': 'Post Processed Message',
                'verbose_name_plural': 'Post Processed Messages',
                'db_table': 'tg_message',
            },
        ),
        migrations.CreateModel(
            name='TGRawMessage',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.BigIntegerField(verbose_name='Chat ID')),
                ('chat_name', models.CharField(max_length=64, null=True, verbose_name='Chat Name')),
                ('username', models.CharField(max_length=64, null=True, verbose_name='Username')),
                ('raw_message', models.TextField(null=True, verbose_name='Raw Text Message')),
                ('date_time', models.DateTimeField(null=True, verbose_name='Create Datetime')),
            ],
            options={
                'verbose_name': 'RAW-message',
                'verbose_name_plural': 'RAW-messages',
                'db_table': 'tg_raw_message',
            },
        ),
        migrations.CreateModel(
            name='TGUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='User ID')),
                ('chat_id', models.BigIntegerField(verbose_name='Chat ID')),
                ('username', models.CharField(max_length=64, null=True, verbose_name='Username')),
            ],
            options={
                'db_table': 'tg_user',
            },
        ),
        migrations.CreateModel(
            name='TGTemplateParseMsg',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Template ID')),
                ('label', models.CharField(max_length=64, verbose_name='Label Post Processing Msg')),
                ('regex', models.TextField(max_length=200, null=True, verbose_name='Regexp')),
                ('condition_type', models.CharField(choices=[('In', 'Include'), ('Ex', 'Exclude')], default='In', max_length=2, null=True, verbose_name='Condition Type')),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.tgchat', verbose_name='Chat ID')),
            ],
            options={
                'verbose_name': 'Template Parse Msg',
                'verbose_name_plural': 'Template Parse Msgs',
                'db_table': 'tg_template_parse_msg',
            },
        ),
    ]