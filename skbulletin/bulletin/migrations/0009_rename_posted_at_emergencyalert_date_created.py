# Generated by Django 5.2 on 2025-05-18 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0008_emergencyalert_description_emergencyalert_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emergencyalert',
            old_name='posted_at',
            new_name='date_created',
        ),
    ]
