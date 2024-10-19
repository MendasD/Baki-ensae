from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.LoginView, name="login"),
    path('compte/', views.SignUpView, name="signup"),
    path('logout/',views.logoutView,name="logout"),
]