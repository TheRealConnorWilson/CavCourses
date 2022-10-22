# Generated by Django 4.2.dev20220917173820 on 2022-10-19 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("classlist", "0009_remove_department_dept_courses"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="facility_description",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="course",
            name="instructor_name",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="course",
            name="intructor_email",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="course",
            name="meeting_days",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]