# Generated by Django 5.0.6 on 2024-07-08 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0005_alter_sujets_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sujets',
            name='annee',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sujets',
            name='classe',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sujets',
            name='matiere',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sujets',
            name='semestre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sujets',
            name='titre',
            field=models.CharField(max_length=50),
        ),
    ]
