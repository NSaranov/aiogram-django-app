# Generated by Django 4.1.3 on 2022-11-25 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_tgtemplateparsemsg_report_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgtemplateparsemsg',
            name='report_type',
            field=models.CharField(blank=True, choices=[('Counter Uniq', 'Counter Uniq'), ('Collector Value', 'Collector Value'), ('', '')], default='', max_length=30, null=True, verbose_name='Report'),
        ),
    ]
