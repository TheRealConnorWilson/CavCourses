# Generated by Django 4.1.1 on 2022-11-01 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_created',
            field=models.BooleanField(default=False),
        ),
    ]
