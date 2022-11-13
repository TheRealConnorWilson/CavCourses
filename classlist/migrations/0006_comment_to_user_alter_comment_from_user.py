# Generated by Django 4.1.3 on 2022-11-13 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classlist', '0005_remove_comment_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='to_user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='schedule_comments', to='classlist.account'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='from_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to='classlist.account'),
        ),
    ]
