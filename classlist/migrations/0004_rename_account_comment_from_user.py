# Generated by Django 4.1.3 on 2022-11-13 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classlist', '0003_account_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='account',
            new_name='from_user',
        ),
    ]
