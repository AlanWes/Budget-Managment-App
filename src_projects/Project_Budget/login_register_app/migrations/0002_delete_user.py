# Generated by Django 4.1.7 on 2023-04-14 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_register_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]