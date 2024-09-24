from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Utilisateur
from .forms import ConnexionForm,CreateCompte
from django.db import IntegrityError  # Importez l'exception d'intégrité de Django
#from channels.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from EducResa import settings 
# Create your views here.


def LoginView(request):
    if request.method=='POST':
        if 'connecter' in request.POST:
            # myform = ConnexionForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
        
        #user = Utilisateur.objects.filter(username=username,password=password,email=email)
        
            try:
                user = Utilisateur.objects.get(username=username)
                if user.password == password and user.email == email:
                    login(request, user.user)#On se connecte avec le user du modele User de Django
                    request.session['user_id'] = user.id #pour creer une session pour l'utilisateur et conserver ses données. On pourra recuperer ces données par la suite et les utiliser
                    nbre_user = Utilisateur.objects.count() #compter le nombre d'utilisateurs
                    return render(request,'index.html',{'user_id': user.id,'user_name': user.username, 'user_email': user.email,'user_photo': user.photo,'nombre_user': nbre_user,'user':user})
                elif user.email != email:
                    error = "Adresse mail incorrect"
                    return render(request, 'login.html', {'error_message':error})
                elif user.password != password:
                    error = "Mot de passe incorrect"
                    return render(request, 'login.html', {'error_message':error})
                
            except Utilisateur.DoesNotExist:
                error = "Vous n'êtes pas enregistré dans notre base, veuillez créer un compte!!!"
                cliquer = "Cliquer ici pour créer un compte"
                return render(request, 'login.html', {'error_message':error, 'cliquer_ici':cliquer})
            

            #if user:
                #request.session['user_id'] = user.id #pour creer une session pour l'utilisateur et conserver ses données
                #return redirect('Home')
        
    else:
        myform = ConnexionForm(request.POST)
        return render(request, 'login.html',{'form':myform})
    
def logoutView(request):
    logout(request)
    return redirect('Login')

def SignUpView(request):
    if request.method == 'POST':
        if 'compte' in request.POST:
            # myform = CreateCompte(request.POST, request.FILES)
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            photo = request.FILES.get('photo') if 'photo' in request.FILES else None
            
        
            try:
                user=User.objects.create_user(
                        username=username,
                        email=email,
                        password=password)#On crée un user avec le modele User de Django (pour l'utiliser a la plateforme de messagerie)

                Utilisateur.objects.create(user=user, username=username, password=password, email=email, photo=photo)
                return redirect('login')
            except IntegrityError:
                message = "Le nom d'utilisateur ou l'adresse email existe déjà."
                return render(request, 'signup.html', {'valide': message})
        
        
    else:
        return render(request, 'signup.html')