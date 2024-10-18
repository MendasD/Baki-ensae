"""
URL configuration for EducResa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home, name="home"),
    path('sujets/', views.create_Sujet, name='poster_sujets'),
    path('Accueil/', views.Index, name='Index'),
    path('comptes/', include("comptes.urls")),
    path('bibliotheque/',views.bibliotheque, name='bibliotheque'),
    path('bibliotheque/ajouterdoc/',views.create_document,name='creer_document'),
    path('Mon_espace/', views.MonEspace, name="mon_espace"),
    path('Modifier_données/',views.ModifierUser, name='modifier_user'),
    path('Nous_contacter/',views.NousContacter, name='nous_contacter'),


    path('documents/download/<str:id_sujet>/', views.Download, name='download'),
    path('documents/divers/download/<str:id_doc>/', views.Downloaddoc, name='downloaddoc'),
    path('documents/download/corriges/<str:id_corrige>/', views.Download_corrige, name='download_corrige'),
    path('documents/corriges/<str:id_sujet>/', views.Poster_corrige, name='poster_corrige'),
    path('documents/corrections/<str:id_sujet>/', views.Voir_correction, name='see_correction'),
    path('documents/sujets/<str:id_sujet>/', views.voir_sujet, name='see_sujet'),
    path('documents/divers/open/<str:id_doc>/', views.voir_document, name='voirdocument'),
    path('documents/corriges_opened/<str:id_corrige>/', views.Voir_corrige, name='see_corrige'),
    path('documents/corriges_deleted/<str:id_corrige>/', views.Supprimer_corrige, name='supprimer_corrige'),

    path('ENSAE/<str:user_email>', views.Ensae, name='Ensae'),
    path('ISSEA/<str:user_email>', views.Issea, name='Issea'),
    path('ENSEA/<str:user_email>', views.Ensea, name='Ensea'),

    path('ENSAE/AS1/', views.Ensaeas1, name='ensae-as1'),
    path('ENSAE/AS2/', views.Ensaeas2, name='ensae-as2'),
    path('ENSAE/AS3/', views.Ensaeas3, name='ensae-as3'),
    path('ENSAE/ISEP1/', views.Ensaeisep1, name='ensae-isep1'),
    path('ENSAE/ISEP2/', views.Ensaeisep2, name='ensae-isep2'),
    path('ENSAE/ISEP3/', views.Ensaeisep3, name='ensae-isep3'),
    path('ENSAE/ISE1-maths/', views.Ensaeise1maths, name='ensae-ise1-maths'),
    path('ENSAE/ISE1-eco/', views.Ensaeise1eco, name='ensae-ise1-eco'),
    path('ENSAE/ISE2/', views.Ensaeise2, name='ensae-ise2'),
    path('ENSAE/ISE3/', views.Ensaeise3, name='ensae-ise3'),

    path('ENSEA/AS1/', views.Enseaas1, name='ensea-as1'),
    path('ENSEA/AS2/', views.Enseaas2, name='ensea-as2'),
    path('ENSEA/AS3/', views.Enseaas3, name='ensea-as3'),
    path('ENSEA/ISE1-maths/', views.Enseaise1maths, name='ensea-ise1-maths'),
     path('ENSEA/ISE1-eco/', views.Enseaise1eco, name='ensea-ise1-eco'),
    path('ENSEA/ISE2/', views.Enseaise2, name='ensea-ise2'),
    path('ENSEA/ISE3/', views.Enseaise3, name='ensea-ise3'),

    path('ISSEA/AS1/', views.Isseaas1, name='issea-as1'),
    path('ISSEA/AS2/', views.Isseaas2, name='issea-as2'),
    path('ISSEA/AS3/', views.Isseaas3, name='issea-as3'),
    path('ISSEA/ISEL1/', views.Isseaisel1, name='issea-isel1'),
    path('ISSEA/ISEL2/', views.Isseaisel2, name='issea-isel2'),
    path('ISSEA/ISEL3/', views.Isseaisel3, name='issea-isel3'),
    path('ISSEA/ISE1-maths/', views.Isseaise1maths, name='issea-ise1-maths'),
    path('ISSEA/ISE1-eco/', views.Isseaise1eco, name='issea-ise1-eco'),
    path('ISSEA/ISE2/', views.Isseaise2, name='issea-ise2'),
    path('ISSEA/ISE3/', views.Isseaise3, name='issea-ise3'),


    path('ENSAE/AS1/Semestre1/', views.Ensaeas1semestre1, name='ensae-as1-semestre1'),
    path('ENSAE/AS1/Semestre2/', views.Ensaeas1semestre2, name='ensae-as1-semestre2'),
    path('ENSAE/AS2/Semestre1/', views.Ensaeas2semestre1, name='ensae-as2-semestre1'),
    path('ENSAE/AS2/Semestre2/', views.Ensaeas2semestre2, name='ensae-as2-semestre2'),
    path('ENSAE/AS3/Semestre1/', views.Ensaeas3semestre1, name='ensae-as3-semestre1'),
    path('ENSAE/AS3/Semestre2/', views.Ensaeas3semestre2, name='ensae-as3-semestre2'),
    path('ENSAE/ISEP1/Semestre1/', views.Ensaeisep1semestre1, name='ensae-isep1-semestre1'),
    path('ENSAE/ISEP1/Semestre2/', views.Ensaeisep1semestre2, name='ensae-isep1-semestre2'),
    path('ENSAE/ISEP2/Semestre1/', views.Ensaeisep2semestre1, name='ensae-isep2-semestre1'),
    path('ENSAE/ISEP2/Semestre2/', views.Ensaeisep2semestre2, name='ensae-isep2-semestre2'),
    path('ENSAE/ISEP3/Semestre1/', views.Ensaeisep3semestre1, name='ensae-isep3-semestre1'),
    path('ENSAE/ISEP3/Semestre2/', views.Ensaeisep3semestre2, name='ensae-isep3-semestre2'),
    path('ENSAE/ISE1-maths/Semestre1/', views.Ensaeise1mathssemestre1, name='ensae-ise1maths-semestre1'),
    path('ENSAE/ISE1-maths/Semestre2/', views.Ensaeise1mathssemestre2, name='ensae-ise1maths-semestre2'),
    path('ENSAE/ISE1-eco/Semestre1/', views.Ensaeise1ecosemestre1, name='ensae-ise1eco-semestre1'),
    path('ENSAE/ISE1-eco/Semestre2/', views.Ensaeise1ecosemestre2, name='ensae-ise1eco-semestre2'),
    path('ENSAE/ISE2/Semestre1/', views.Ensaeise2semestre1, name='ensae-ise2-semestre1'),
    path('ENSAE/ISE2/Semestre2/', views.Ensaeise2semestre2, name='ensae-ise2-semestre2'),
    path('ENSAE/ISE3/Semestre1/', views.Ensaeise3semestre1, name='ensae-ise3-semestre1'),
    path('ENSAE/ISE3/Semestre2/', views.Ensaeise3semestre2, name='ensae-ise3-semestre2'),

    path('ENSEA/AS1/Semestre1/', views.Enseaas1semestre1, name='ensea-as1-semestre1'),
    path('ENSEA/AS1/Semestre2/', views.Enseaas1semestre2, name='ensea-as1-semestre2'),
    path('ENSEA/AS2/Semestre1/', views.Enseaas2semestre1, name='ensea-as2-semestre1'),
    path('ENSEA/AS2/Semestre2/', views.Enseaas2semestre2, name='ensea-as2-semestre2'),
    path('ENSEA/AS3/Semestre1/', views.Enseaas3semestre1, name='ensea-as3-semestre1'),
    path('ENSEA/AS3/Semestre2/', views.Enseaas3semestre2, name='ensea-as3-semestre2'),
    path('ENSEA/ISE1-maths/Semestre1/', views.Enseaise1mathssemestre1, name='ensea-ise1maths-semestre1'),
    path('ENSEA/ISE1-maths/Semestre2/', views.Enseaise1mathssemestre2, name='ensea-ise1maths-semestre2'),
    path('ENSEA/ISE1-eco/Semestre1/', views.Enseaise1ecosemestre1, name='ensea-ise1eco-semestre1'),
    path('ENSEA/ISE1-eco/Semestre2/', views.Enseaise1ecosemestre2, name='ensea-ise1eco-semestre2'),
    path('ENSEA/ISE2/Semestre1/', views.Enseaise2semestre1, name='ensea-ise2-semestre1'),
    path('ENSEA/ISE2/Semestre2/', views.Enseaise2semestre2, name='ensea-ise2-semestre2'),
    path('ENSEA/ISE3/Semestre1/', views.Enseaise3semestre1, name='ensea-ise3-semestre1'),
    path('ENSEA/ISE3/Semestre2/', views.Enseaise3semestre2, name='ensea-ise3-semestre2'),

    path('ISSEA/AS1/Semestre1/', views.Isseaas1semestre1, name='issea-as1-semestre1'),
    path('ISSEA/AS1/Semestre2/', views.Isseaas1semestre2, name='issea-as1-semestre2'),
    path('ISSEA/AS2/Semestre1/', views.Isseaas2semestre1, name='issea-as2-semestre1'),
    path('ISSEA/AS2/Semestre2/', views.Isseaas2semestre2, name='issea-as2-semestre2'),
    path('ISSEA/AS3/Semestre1/', views.Isseaas3semestre1, name='issea-as3-semestre1'),
    path('ISSEA/AS3/Semestre2/', views.Isseaas3semestre2, name='issea-as3-semestre2'),
    path('ISSEA/ISEL1/Semestre1/', views.Isseaisel1semestre1, name='issea-isel1-semestre1'),
    path('ISSEA/ISEL1/Semestre2/', views.Isseaisel1semestre2, name='issea-isel1-semestre2'),
    path('ISSEA/ISEL2/Semestre1/', views.Isseaisel2semestre1, name='issea-isel2-semestre1'),
    path('ISSEA/ISEL3/Semestre2/', views.Isseaisel3semestre2, name='issea-isel3-semestre2'),
    path('ISSEA/ISEL3/Semestre1/', views.Isseaisel3semestre1, name='issea-isel3-semestre1'),
    path('ISSEA/ISEL2/Semestre2/', views.Isseaisel2semestre2, name='issea-isel2-semestre2'),
    path('ISSEA/ISE1-maths/Semestre1/', views.Isseaise1mathssemestre1, name='issea-ise1maths-semestre1'),
    path('ISSEA/ISE1-maths/Semestre2/', views.Isseaise1mathssemestre2, name='issea-ise1maths-semestre2'),
    path('ISSEA/ISE1-eco/Semestre1/', views.Isseaise1ecosemestre1, name='issea-ise1eco-semestre1'),
    path('ISSEA/ISE1-eco/Semestre2/', views.Isseaise1ecosemestre2, name='issea-ise1eco-semestre2'),
    path('ISSEA/ISE2/Semestre1/', views.Isseaise2semestre1, name='issea-ise2-semestre1'),
    path('ISSEA/ISE2/Semestre2/', views.Isseaise2semestre2, name='issea-ise2-semestre2'),
    path('ISSEA/ISE3/Semestre1/', views.Isseaise3semestre1, name='issea-ise3-semestre1'),
    path('ISSEA/ISE3/Semestre2/', views.Isseaise3semestre2, name='issea-ise3-semestre2'),
    
]


# En cas de DEBUG, on ajoute le chemin pour les fichiers medias (Là se trouvent les photos d'utilisateurs)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
