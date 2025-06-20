# Generated by Django 5.1.1 on 2025-06-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegramuser',
            old_name='created_at',
            new_name='date_joined',
        ),
        migrations.RenameField(
            model_name='telegramuser',
            old_name='user_id',
            new_name='telegram_id',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='last_seen',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
