# Generated by Django 5.1.1 on 2024-10-09 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitas', '0002_visita_cidade_visita_região'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visita',
            old_name='região',
            new_name='regiao',
        ),
    ]
