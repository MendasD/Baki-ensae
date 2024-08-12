from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib import admin
# from Library.models import Document, Vente
from .models import Utilisateur, Sujets, Corriges, Documents


# Pour enregistrer des modèles sur l'interface admin de django
admin.site.register(Utilisateur)
admin.site.register(Sujets)
admin.site.register(Corriges)
admin.site.register(Documents)
