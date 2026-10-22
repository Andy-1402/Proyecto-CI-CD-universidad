# Migracion inicial de la app gestion (Estudiante y Curso)

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, unique=True)),
                ('nombre', models.CharField(max_length=120)),
                ('creditos', models.PositiveSmallIntegerField(default=3)),
                ('cupo_maximo', models.PositiveSmallIntegerField(default=30)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('nombres', models.CharField(max_length=80)),
                ('apellidos', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('cursos', models.ManyToManyField(blank=True, related_name='estudiantes', to='gestion.curso')),
            ],
            options={
                'verbose_name': 'Estudiante',
                'verbose_name_plural': 'Estudiantes',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
    ]
