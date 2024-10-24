from django.db import models
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.

class Utilisateur (models.Model) :
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='utilisateur',null=True,blank=True)
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 250, unique = True)
    photo = models.ImageField(upload_to = 'documents/photosUsers/', blank = True, default='documents/photosUsers/IMG_20230719_212156_362.jpg')

    def __str__(self) :
        return self.username


class Sujets(models.Model):

    id = models.AutoField(primary_key=True)
    ecole = models.CharField(max_length=50,choices=[('ENSAE', 'ENSAE'), ('ISSEA', 'ISSEA'), ('ENSEA', 'ENSEA')])
    classe = models.CharField(max_length=50, choices=[('AS1', 'AS1'), ('AS2', 'AS2'), ('AS3', 'AS3'),('ISEP1','ISEP1'),('ISEL1','ISEL1'),('ISEP2','ISEP2'),('ISEL2','ISEL2'),('ISEP3','ISEP3'),('ISEL3','ISEL3'),('ISE1_maths','ISE1_maths'),('ISE1_eco','ISE1_eco'),('ISE2','ISE2'),('ISE3','ISE3')])
    semestre = models.CharField(max_length=50, choices=[('Semestre 1', 'Semestre 1'), ('Semestre 2', 'Semestre 2')])
    matiere = models.CharField(max_length=50)
    titre = models.CharField(max_length=50,null=True,blank=True)
    annee = models.CharField(max_length=50)
    date_upload = models.DateField(auto_now_add=True)
    doc = models.FileField(upload_to='Anciens_Sujets/',unique=True, blank=True) # Pour des raisons de telechargement du fichier

    def __str__(self):
        return self.titre

class Corriges(models.Model):

    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    doc = models.FileField(upload_to='Corriges/',unique=True, blank=True)
    description = models.TextField(max_length=1000)
    sujets = models.ForeignKey(Sujets, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Documents(models.Model):
    id = models.AutoField(primary_key=True)
    matiere = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    classe = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    fichier = models.FileField(upload_to='DocumentsDivers/', unique=True)
    description = models.TextField(max_length=1000)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
