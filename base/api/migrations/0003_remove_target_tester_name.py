# Generated by Django 4.2.8 on 2023-12-06 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_target_tuser_rename_tester_mail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targets',
            name='tester_name',
        ),
    ]
