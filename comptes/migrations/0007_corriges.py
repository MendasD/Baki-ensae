# Generated by Django 5.0.6 on 2024-07-08 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0006_alter_sujets_annee_alter_sujets_classe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corriges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
                ('doc', models.FileField(blank=True, upload_to='Corriges/')),
                ('description', models.TextField(max_length=1000)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comptes.utilisateur')),
                ('sujets', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comptes.sujets')),
            ],
        ),
    ]
