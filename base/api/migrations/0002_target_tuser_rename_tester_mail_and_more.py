# Generated by Django 4.2.8 on 2023-12-06 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tester_name', models.CharField(max_length=255)),
                ('tname', models.CharField(max_length=255)),
                ('madr', models.CharField(max_length=255)),
                ('dadr', models.CharField(max_length=255)),
                ('rem', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targets', models.CharField(max_length=255)),
                ('ulogin', models.CharField(max_length=255)),
                ('upass', models.CharField(max_length=255)),
                ('uorg', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameModel(
            old_name='Tester',
            new_name='Mail',
        ),
        migrations.RenameField(
            model_name='mail',
            old_name='tester_name',
            new_name='tmail',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='location',
            new_name='test_grp',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='steps_list_of_jsons',
            new_name='test_text',
        ),
        migrations.RemoveField(
            model_name='test',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='test',
            name='tester',
        ),
        migrations.RemoveField(
            model_name='test',
            name='total_steps',
        ),
        migrations.AlterField(
            model_name='test',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
