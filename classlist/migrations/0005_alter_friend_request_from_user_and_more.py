# Generated by Django 4.1.1 on 2022-11-01 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classlist', '0004_user_friends_user_schedule_friend_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='from_user',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='friend_request',
            name='to_user',
            field=models.IntegerField(default=0),
        ),
    ]
