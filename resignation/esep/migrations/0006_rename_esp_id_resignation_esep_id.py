# Generated by Django 4.2.4 on 2023-09-04 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esep', '0005_resignation_first_name_resignation_last_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resignation',
            old_name='esp_id',
            new_name='esep_id',
        ),
    ]