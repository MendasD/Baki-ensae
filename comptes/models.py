from django.db import models
from django.conf import settings

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
    ecole = models.CharField(max_length=50)
    classe = models.CharField(max_length=50)
    semestre = models.CharField(max_length=50)
    matiere = models.CharField(max_length=50)
    titre = models.CharField(max_length=50)
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
