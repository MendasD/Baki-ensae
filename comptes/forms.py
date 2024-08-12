from django import forms
from .models import Utilisateur
from django.contrib.auth.models import User


class ConnexionForm(forms.ModelForm):
    class Meta: # si on veut creer un formulaire qui ne depend pas d'un modele dejà defini, on a pas besoin de cela. On pourra directement definir les differents champs
        model = Utilisateur
        fields=['username','email','password']
        widgets = {
            'password': forms.PasswordInput(),
        } # ça c'est pour specifier que la saisie sera un mot de passe donc, sera caché

class CreateCompte(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields=['username','email','password','photo']
        widgets = {
            'password': forms.PasswordInput(),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
        }

