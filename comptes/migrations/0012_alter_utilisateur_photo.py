# Generated by Django 4.0.6 on 2024-10-20 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0011_auto_20241018_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='photo',
            field=models.ImageField(blank=True, default='documents/documents/photosUsers/IMG_20230719_212156_362.jpg', upload_to='documents/documents/photosUsers/'),
        ),
    ]
