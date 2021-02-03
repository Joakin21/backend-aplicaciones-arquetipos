# Generated by Django 2.2.12 on 2021-02-03 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import editor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfesionalSalud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profesion', models.CharField(max_length=50)),
                ('centro_salud', models.CharField(max_length=50)),
                ('listas_arquetipos', djongo.models.fields.ArrayField(model_container=editor.models.ListaArquetipos, model_form_class=editor.models.ListaArquetiposForm)),
                ('ultimos_pacientes_atendidos', djongo.models.fields.ArrayField(model_container=editor.models.UltimosPacientesAtendidos, model_form_class=editor.models.UltimosPacientesAtendidosForm)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
