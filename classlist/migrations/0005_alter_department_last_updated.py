# Generated by Django 4.2.dev20220917173820 on 2022-11-10 19:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("classlist", "0004_department_last_updated_alter_account_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="last_updated",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="last updated"
            ),
        ),
    ]
