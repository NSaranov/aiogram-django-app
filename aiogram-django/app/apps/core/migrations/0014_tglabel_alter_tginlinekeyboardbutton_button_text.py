# Generated by Django 4.1.3 on 2022-11-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_tginlinekeyboardbutton'),
    ]

    operations = [
        migrations.CreateModel(
            name='TGLabel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('lable', models.CharField(max_length=50, null=True, verbose_name='Lable')),
            ],
            options={
                'verbose_name': 'Label Post Processing Msg',
                'verbose_name_plural': 'Labels Post Processing Msg',
                'db_table': 'tg_label',
            },
        ),
        migrations.AlterField(
            model_name='tginlinekeyboardbutton',
            name='button_text',
            field=models.CharField(max_length=50, null=True, verbose_name='Button Text'),
        ),
    ]
