# Generated by Django 5.1.4 on 2024-12-11 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0006_alter_clientecursos_tipo_aquisicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientecursos',
            name='tipo_aquisicao',
            field=models.CharField(choices=[('Ganhado', 'Vip'), ('Comprado', 'Comprado')], default='Comprado', max_length=20),
        ),
    ]
