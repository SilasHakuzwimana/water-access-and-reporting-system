# Generated by Django 5.1.4 on 2024-12-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wars', '0007_rename_national_id_warsuser_nationalid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warsuser',
            name='nationalId',
            field=models.CharField(max_length=16),
        ),
    ]
