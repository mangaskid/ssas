# Generated by Django 3.2.16 on 2023-03-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_attendance_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='is_confirm',
            field=models.BooleanField(default=False),
        ),
    ]
