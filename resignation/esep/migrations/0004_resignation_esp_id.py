# Generated by Django 4.2.4 on 2023-09-04 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esep', '0003_alter_resignation_manager_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='resignation',
            name='esp_id',
            field=models.CharField(null=True),
        ),
    ]