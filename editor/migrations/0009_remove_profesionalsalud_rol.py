# Generated by Django 2.2.12 on 2020-07-09 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0008_auto_20200709_1243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profesionalsalud',
            name='rol',
        ),
    ]