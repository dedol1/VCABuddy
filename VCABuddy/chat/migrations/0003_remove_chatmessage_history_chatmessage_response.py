# Generated by Django 4.2.5 on 2023-09-12 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='history',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='response',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
