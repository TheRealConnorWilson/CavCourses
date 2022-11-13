# Generated by Django 4.1.3 on 2022-11-13 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250)),
                ('account', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='classlist.account')),
                ('schedule', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='classlist.schedule')),
            ],
        ),
    ]