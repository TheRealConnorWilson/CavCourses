# Generated by Django 4.2.dev20220917173820 on 2022-11-05 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classlist", "0004_alter_schedule_fri_alter_schedule_mon_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="profile_picture",
            field=models.TextField(blank=True, null=True),
        ),
    ]
