# Generated by Django 2.2.12 on 2020-07-09 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0003_profesionalsalud_centro_salud'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesionalsalud',
            name='rol',
            field=models.IntegerField(null=True),
        ),
    ]