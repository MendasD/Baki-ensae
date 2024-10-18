from django.contrib import admin
from .models import Utilisateur, Sujets, Corriges, Documents


# Register your models here.

class SujetsAdmin(admin.ModelAdmin):
    list_display = ('ecole', 'classe', 'semestre','matiere','titre','annee')


# Pour enregistrer des modèles sur l'interface admin de django
admin.site.register(Utilisateur)
admin.site.register(Sujets,SujetsAdmin)
admin.site.register(Corriges)
admin.site.register(Documents)
