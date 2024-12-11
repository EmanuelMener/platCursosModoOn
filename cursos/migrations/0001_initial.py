# Generated by Django 5.1.4 on 2024-12-09 19:25

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
                ('nome', models.CharField(max_length=255)),
                ('horario', models.CharField(max_length=100)),
                ('local', models.CharField(max_length=100)),
                ('numero_alunos', models.IntegerField()),
                ('codigo', models.CharField(max_length=50)),
                ('turma', models.CharField(max_length=50)),
                ('semestre', models.CharField(max_length=50)),
                ('capa', models.ImageField(upload_to='cursos/capas/')),
            ],
        ),
    ]
