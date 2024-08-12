from django import forms
from comptes.models import Sujets,Corriges,Documents

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Sujets
        fields = ['ecole','classe','semestre','matiere','titre','annee','doc']
        widgets = {
            'doc': forms.FileInput(attrs={'accept': 'image/*,application/pdf, text/plain'}),
        }

class CorrigesForm(forms.ModelForm):
    class Meta:
        model = Corriges
        exclude = ['auteur', 'sujets']
        fields = ['titre','doc','description']
        widgets = {
            'doc': forms.FileInput(attrs={'accept': 'image/*,application/pdf, text/plain'}),
        }

class CreateDocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields=['matiere','type','classe','fichier','description',]
        widgets = {
            'fichier': forms.FileInput(attrs={'accept': 'application/pdf, image/*'}),
        }