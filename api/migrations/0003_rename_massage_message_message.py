# Generated by Django 4.1.5 on 2023-01-11 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_token_user_token"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="massage",
            new_name="message",
        ),
    ]