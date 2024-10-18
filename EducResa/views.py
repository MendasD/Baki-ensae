from django.shortcuts import render
from django.http import HttpResponse, Http404,FileResponse,HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import os
from comptes.models import Sujets,Utilisateur,Corriges,Documents
from .forms import DocumentForm,CorrigesForm, CreateDocumentForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from EducResa import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login



def Home(request) :
    return render(request, 'home.html') # 'locals' permet de creer un dictionnaire a partir des variables declarees. on aurait pu faire un dictionnaire nous meme et ne pas utiliser locals : {'utilisateur': username, 'nb_sujets': nb_sujets, 'nb_cours': nb_cours}

def Index(request) :
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    nbre_user = Utilisateur.objects.count() #compter le nombre d'utilisateurs
    return render(request, 'index.html', {'user': user,'user_email': user.email,'nombre_user': nbre_user})

def Sujet(request) :
    if request.method == 'POST':
        ecole = request.POST.get('ecole')
        annee = request.POST.get('annee')
        semestre = request.POST.get('semestre')
        titre = request.POST.get('titre')
        matiere = request.POST.get('matiere')
        doc= request.FILES.get('doc') if 'doc' in request.FILES else None
        try :
            newsujet = Sujets.objects.create(
                ecole=ecole,
                annee=annee,
                semestre=semestre,
                titre=titre,
                matiere=matiere,
                doc=doc
            )
            print("Données enregistrées")
            return redirect('Sujets.html')  # pour renenir sur le formulaire
        except Exception as e:
            print(f"Erreur lors de la création du sujet: {e}")
            
    else:
        return render(request, 'Sujets.html')
    

def create_Sujet(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('.')  # pour renenir sur le formulaire
    else:
        form = DocumentForm()
    return render(request, 'Sujets.html', {'form': form})

def create_document(request):
    if request.method == 'POST':
        form = CreateDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.auteur = Utilisateur.objects.get(id=request.session.get('user_id'))
            doc.save()
            return redirect('.')
    else:
        form = CreateDocumentForm()
        user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'documents_divers.html', {'form': form, 'user': user})

def bibliotheque(request):
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    documents = Documents.objects.all().order_by('-date')
    nombre = Documents.objects.count()
    return render(request, 'bibliotheque.html', {'user': user, 'documents': documents, 'nombre': nombre})

def Download(request, id_sujet):
    document = get_object_or_404(Sujets, id=id_sujet)
    file_path = document.doc.path  # on recupere le chemin du fichier à telecharger, en respectant les noms utilisés dans la definition du modèle Document
    if os.path.exists(file_path): # On verifie si le fichier existe
        with open(file_path, 'rb') as fh: # On ouvre le fichier en mode lecture binaire
            response = HttpResponse(fh.read(), content_type="application/octet-stream") # Crée une réponse HTTP avec le contenu binaire lu à partir du fichier. Le type de contenu est défini comme application/octet-stream, ce qui indique que le contenu est un flux de données binaires.
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}' # Définit l'en-tête Content-Disposition pour forcer le navigateur à télécharger le fichier plutôt que de l'afficher dans le navigateur. os.path.basename(file_path) est utilisé pour obtenir le nom de fichier à partir du chemin complet.
            return response # Retourne la réponse HTTP prête pour le téléchargement du fichier.
    return redirect('.')

def Downloaddoc(request, id_doc):
    document = get_object_or_404(Documents, id=id_doc)
    file_path = document.fichier.path  # on recupere le chemin du fichier à telecharger, en respectant les noms utilisés dans la definition du modèle Document
    if os.path.exists(file_path): # On verifie si le fichier existe
        with open(file_path, 'rb') as fh: # On ouvre le fichier en mode lecture binaire
            response = HttpResponse(fh.read(), content_type="application/octet-stream") # Crée une réponse HTTP avec le contenu binaire lu à partir du fichier. Le type de contenu est défini comme application/octet-stream, ce qui indique que le contenu est un flux de données binaires.
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response # Retourne la réponse HTTP prête pour le téléchargement du fichier.
    return redirect('.')

def voir_sujet(request, id_sujet):
    sujet = get_object_or_404(Sujets, id=id_sujet)
    file_path = sujet.doc.path

    # Définir le type de contenu en fonction de l'extension du fichier
    if file_path.endswith('.pdf'):
        content_type = 'application/pdf'
    elif file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        content_type = 'image/*'
    elif file_path.endswith('.txt'):
        content_type = 'text/plain'
    else:
        content_type = 'application/octet-stream'  # Type par défaut pour les fichiers binaires

    response = FileResponse(sujet.doc.open(), content_type=content_type)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(sujet.doc.name)
    return response

def voir_document(request, id_doc):
    document = get_object_or_404(Documents, id=id_doc)
    file_path = document.fichier.path
    # Définir le type de contenu en fonction de l'extension du fichier
    if file_path.endswith('.pdf'):
        content_type = 'application/pdf'
    elif file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        content_type = 'image/*'
    elif file_path.endswith('.txt'):
        content_type = 'text/plain'
    else:
        content_type = 'application/octet-stream'  # Type par défaut pour les fichiers binaires
    
    response = FileResponse(document.fichier.open(), content_type=content_type)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(document.fichier.name)
    return response

def Poster_corrige(request,id_sujet):
    if request.method == 'POST':
        form = CorrigesForm(request.POST, request.FILES)
        if form.is_valid():
            corrige = form.save(commit=False)
            corrige.auteur = Utilisateur.objects.get(id=request.session.get('user_id'))
            corrige.sujets = Sujets.objects.get(id=id_sujet)
            corrige.save()
            return redirect('.',{'id_sujet':id_sujet})  # pour renenir sur le formulaire
    else:
        form = CorrigesForm()
    return render(request, 'poster_corrige.html', {'form': form,'user': Utilisateur.objects.get(id=request.session.get('user_id'))})

def Voir_correction(request, id_sujet):
    sujet = get_object_or_404(Sujets, id=id_sujet)
    corriges = Corriges.objects.filter(sujets=sujet).order_by('-date')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'voir_corrige.html', {'corriges': corriges, 'sujet': sujet,'user': user})

def Voir_corrige(request, id_corrige):
    corrige = get_object_or_404(Corriges, id=id_corrige)
    file_path = corrige.doc.path

    # Définir le type de contenu en fonction de l'extension du fichier
    if file_path.endswith('.pdf'):
        content_type = 'application/pdf'
    elif file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        content_type = 'image/*'
    elif file_path.endswith('.txt'):
        content_type = 'text/plain'
    else:
        content_type = 'application/octet-stream'  # Type par défaut pour les fichiers binaires

    response = FileResponse(corrige.doc.open(), content_type=content_type)
    response['Content-Disposition'] = 'inline; filename="{}"'.format(corrige.doc.name)
    return response


def Download_corrige(request, id_corrige):
    document = get_object_or_404(Corriges, id=id_corrige)
    file_path = document.doc.path # on recupere le chemin du fichier à telecharger, en respectant les noms utilisés dans la definition du modèle Document
    if os.path.exists(file_path): # On verifie si le fichier existe
        with open(file_path, 'rb') as fh: # On ouvre le fichier en mode lecture binaire
            response = HttpResponse(fh.read(), content_type="application/octet-stream") # Crée une réponse HTTP avec le contenu binaire lu à partir du fichier. Le type de contenu est défini comme application/octet-stream, ce qui indique que le contenu est un flux de données binaires.
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}' # Définit l'en-tête Content-Disposition pour forcer le navigateur à télécharger le fichier plutôt que de l'afficher dans le navigateur. os.path.basename(file_path) est utilisé pour obtenir le nom de fichier à partir du chemin complet.
            return response # Retourne la réponse HTTP prête pour le téléchargement du fichier.
    return redirect('.')


def Supprimer_corrige(request, id_corrige):
    corrige = get_object_or_404(Corriges, id=id_corrige)
    corrige.delete()
    sujet = corrige.sujets
    corriges = Corriges.objects.filter(sujets=corrige.sujets).order_by('-date')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'voir_corrige.html', {'corriges': corriges, 'sujet': sujet,'user': user})



# ECOLES
def Ensae(request, user_email) :
    user = Utilisateur.objects.get(email=user_email)
    return render(request, 'ensae.html', {'user_email': user_email, 'user': user})

def Issea(request, user_email) :
    user = Utilisateur.objects.get(email=user_email)
    return render(request, 'issea.html', {'user_email': user_email, 'user': user})

def Ensea(request, user_email) :
    user = Utilisateur.objects.get(email=user_email)
    return render(request, 'ensea.html', {'user_email': user_email,'user':user})

# ENSAE/classes
def Ensaeas1(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeas1.html',{'user':user})

def Ensaeas2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeas2.html', {'user':user})

def Ensaeas3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeas3.html', {'user':user})

def Ensaeisep1(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeisep1.html',{'user':user})

def Ensaeisep2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeisep2.html',{'user':user})

def Ensaeisep3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeisep3.html',{'user':user})

def Ensaeise1maths(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeise1maths.html',{'user':user})

def Ensaeise1eco(request):
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeise1eco.html', {'user':user})

def Ensaeise2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeise2.html',{'user':user})

def Ensaeise3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'ensaeise3.html',{'user':user})


# ENSEA/classes
def Enseaas1(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaas1.html',{'user':user})

def Enseaas2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaas2.html', {'user':user})

def Enseaas3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaas3.html', {'user':user})

def Enseaise1maths(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaise1maths.html',{'user':user})

def Enseaise1eco(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaise1eco.html',{'user':user})

def Enseaise2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaise2.html',{'user':user})

def Enseaise3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'enseaise3.html',{'user':user})


# ISSEA/classes
def Isseaas1(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaas1.html',{'user':user})

def Isseaas2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaas2.html', {'user':user})

def Isseaas3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaas3.html', {'user':user})

def Isseaisel1(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaisel1.html',{'user':user})

def Isseaisel2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaisel2.html',{'user':user})

def Isseaisel3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaisel3.html',{'user':user})

def Isseaise1maths(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaise1maths.html',{'user':user})

def Isseaise1eco(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaise1eco.html',{'user':user})

def Isseaise2(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaise2.html',{'user':user})

def Isseaise3(request) :
    user_id = request.session.get('user_id')
    user = Utilisateur.objects.get(id=user_id)
    return render(request, 'isseaise3.html',{'user':user})



# ENSAE/AS1/semestres
def Ensaeas1semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='AS1', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeas1semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeas1semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='AS1', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeas1semestre2.html',{'sujets':sujets,'user':user})


# ENSAE/AS2/semestres
def Ensaeas2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='AS2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeas2semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeas2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='AS2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeas2semestre2.html',{'sujets':sujets,'user':user})


# ENSAE/AS3/semestres
def Ensaeas3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='AS3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeas3semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeas3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='AS3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeas1semestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISEP1/semestres
def Ensaeisep1semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISEP1', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeisep1semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeisep1semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISEP1', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeisep1semestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISEP2/semestres
def Ensaeisep2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISEP2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeisep2semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeisep2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISEP2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeisep2semestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISEP3/semestres
def Ensaeisep3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISEP3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeisep3semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeisep3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISEP2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeisep3semestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISE1-maths/semestres
def Ensaeise1mathssemestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE1_maths', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise1mathssemestre1.html', { 'sujets': sujets,'user': user})

def Ensaeise1mathssemestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE1_maths', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise1mathssemestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISE1-eco/semestres
def Ensaeise1ecosemestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE1_eco', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise1ecosemestre1.html', { 'sujets': sujets,'user': user})

def Ensaeise1ecosemestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE1_eco', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise1ecosemestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISE2/semestres
def Ensaeise2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise2semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeise2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise2semestre2.html',{'sujets':sujets,'user':user})

# ENSAE/ISE3/semestres
def Ensaeise3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise1semestre1.html', { 'sujets': sujets,'user': user})

def Ensaeise3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSAE', classe='ISE3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'ensaeise3semestre2.html',{'sujets':sujets,'user':user})


# ENSEA/AS1/semestres
def Enseaas1semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='AS1', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaas1semestre1.html', { 'sujets': sujets,'user': user})

def Enseaas1semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='AS1', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaas1semestre2.html',{'sujets':sujets,'user':user})


# ENSEA/AS2/semestres
def Enseaas2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='AS2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaas2semestre1.html', { 'sujets': sujets,'user': user})

def Enseaas2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='AS2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaas2semestre2.html',{'sujets':sujets,'user':user})


# ENSEA/AS3/semestres
def Enseaas3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='AS3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaas3semestre1.html', { 'sujets': sujets,'user': user})

def Enseaas3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='AS3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaas3semestre2.html',{'sujets':sujets,'user':user})


# ENSEA/ISE1-maths/semestres
def Enseaise1mathssemestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE1_maths', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise1mathssemestre1.html', { 'sujets': sujets,'user': user})

def Enseaise1mathssemestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE1_maths', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise1mathssemestre2.html',{'sujets':sujets,'user':user})

# ENSEA/ISE1-eco/semestres
def Enseaise1ecosemestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE1_eco', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise1ecosemestre1.html', { 'sujets': sujets,'user': user})

def Enseaise1ecosemestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE1_eco', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise1ecosemestre2.html',{'sujets':sujets,'user':user})

# ENSEA/ISE2/semestres
def Enseaise2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise2semestre1.html', { 'sujets': sujets,'user': user})

def Enseaise2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise2semestre2.html',{'sujets':sujets,'user':user})

# ENSEA/ISE3/semestres
def Enseaise3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise1semestre1.html', { 'sujets': sujets,'user': user})

def Enseaise3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ENSEA', classe='ISE3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'enseaise3semestre2.html',{'sujets':sujets,'user':user})



# ISSEA/AS1/semestres
def Isseaas1semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='AS1', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaas1semestre1.html', { 'sujets': sujets,'user': user})

def Isseaas1semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='AS1', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaas1semestre2.html',{'sujets':sujets,'user':user})


# issea/AS2/semestres
def Isseaas2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='AS2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaas2semestre1.html', { 'sujets': sujets,'user': user})

def Isseaas2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='AS2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaas2semestre2.html',{'sujets':sujets,'user':user})


# issea/AS3/semestres
def Isseaas3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='AS3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaas3semestre1.html', { 'sujets': sujets,'user': user})

def Isseaas3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='AS3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaas1semestre2.html',{'sujets':sujets,'user':user})

# issea/ISEL1/semestres
def Isseaisel1semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISEL1', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaisel1semestre1.html', { 'sujets': sujets,'user': user})

def Isseaisel1semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISEL1', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaisel1semestre2.html',{'sujets':sujets,'user':user})

# issea/ISEL2/semestres
def Isseaisel2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISEL2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaisel2semestre1.html', { 'sujets': sujets,'user': user})

def Isseaisel2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISEL2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaisel2semestre2.html',{'sujets':sujets,'user':user})

# issea/ISEL3/semestres
def Isseaisel3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISEL3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    texte = "ISSEA ISEL3 Semestre 1"
    return render(request, 'sujetsemestre.html', { 'sujets': sujets,'user': user,'texte':texte})

def Isseaisel3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISEl3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    texte = "ISSEA ISEL3 Semestre 2"
    return render(request, 'sujetsemestre.html',{'sujets':sujets,'user':user,'texte':texte})

# issea/ISE1-maths/semestres
def Isseaise1mathssemestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE1_maths', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    texte = "ISSEA ISE1 option Mathématiques Semestre 1"
    return render(request, 'sujetsemestre.html', { 'sujets': sujets,'user': user,'texte':texte})

def Isseaise1mathssemestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE1_maths', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    texte = "ISSEA ISE1 option Mathématiques Semestre 2"
    return render(request, 'isseaise1mathssemestre2.html',{'sujets':sujets,'user':user,'texte':texte})

# issea/ISE1-eco/semestres
def Isseaise1ecosemestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE1_eco', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    texte = "ISSEA ISE1 option Economie Semestre 1"
    return render(request, 'sujetsemestre.html', { 'sujets': sujets,'user': user,'texte':texte})

def Isseaise1ecosemestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE1_eco', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    texte = "ISSEA ISE1 option Economie Semestre 2"
    return render(request, 'sujetsemestre.html',{'sujets':sujets,'user':user,'texte':texte})

# issea/ISE2/semestres
def Isseaise2semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE2', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaise2semestre1.html', { 'sujets': sujets,'user': user})

def Isseaise2semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE2', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaise2semestre2.html',{'sujets':sujets,'user':user})

# issea/ISE3/semestres
def Isseaise3semestre1(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE3', semestre='Semestre 1').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaise1semestre1.html', { 'sujets': sujets,'user': user})

def Isseaise3semestre2(request) :
    sujets = Sujets.objects.filter(ecole='ISSEA', classe='ISE3', semestre='Semestre 2').order_by('-date_upload')
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    return render(request, 'isseaise3semestre2.html',{'sujets':sujets,'user':user})

def MonEspace(request):
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    corriges = Corriges.objects.filter(auteur=user).order_by('-date')
    documents = Documents.objects.filter(auteur=user).order_by('-date')
    tous_documents = Documents.objects.all()
    tous_corriges = Corriges.objects.all()
    
    if tous_corriges.count() != 0:
        pourcentage_corriges = round((corriges.count() / tous_corriges.count()) * 100, 2)
    else:
        pourcentage_corriges = 0
    if tous_documents.count() != 0:  
        pourcentage_document = round((documents.count() / tous_documents.count()) * 100, 2)
    else:
        pourcentage_document = 0

    nbcorriges = corriges.count()
    nbdocuments = documents.count()
    return render(request, 'monespace.html', {'user': user, 'corriges': corriges, 'documents': documents, 'nombre_corriges': nbcorriges, 'nombre_doc': nbdocuments, 'p_message': '', 'p_doc': pourcentage_document, 'p_corrige': pourcentage_corriges})

@csrf_exempt
def ModifierUser(request):
    if request.method == 'POST':
        try:
            
            data = request.POST  # Utilisation de request.POST pour les données textuelles
            photo = request.FILES.get('photo')  # Récupération du fichier photo si présent
            
            username = data.get('username',"")
            email = data.get('email', "")
            password = data.get('password', "")
            user_id = request.session.get('user_id')
            try:
                user = Utilisateur.objects.get(id=user_id)
                # Mise à jour des informations dans le modèle Utilisateur
                user.username = username
                user.email = email
                user.photo = photo

                # Mise à jour des informations dans le modèle User (Django)
                if user.user:
                    user.user.username = username
                    user.user.email = email

                    if password:  # Mettez à jour le mot de passe seulement s'il est fourni
                        user.user.set_password(password)

                    user.user.save()

                user.save()  # Sauvegarder les changements dans le modèle Utilisateur
                login(request, user.user)
                request.session['user_id'] = user.id
                
                return JsonResponse({'status': 'success'})
            except Utilisateur.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        except Exception as e:
            print('probleme')
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def NousContacter(request):
    user = Utilisateur.objects.get(id=request.session.get('user_id'))
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        # Compose the email
        full_message = f"Message de {name} ({email}):\n\n{message}"

        # envoi de l'email
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,  
            [settings.CONTACT_EMAIL],  
        )

        return redirect('.')  

    return render(request, 'nouscontacter.html', {'user': user})
