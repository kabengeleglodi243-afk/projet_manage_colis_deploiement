"""
URL configuration for gestion_colis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from app.views import connexion, register, enregistrer_colis, lister_colis, suivre_colis, detail_colis, modifier_colis, supprimer_colis, deconnexion

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', connexion, name="connexion"),
    path('register/', register, name="register"),
    path('enregistrer_colis/', enregistrer_colis, name="enregistrer_colis"),
    path('lister_colis/', lister_colis, name="lister_colis"),
    path('detail_colis/<int:id>/', detail_colis, name="detail_colis"),
    path('modifier_colis/<int:id>/', modifier_colis, name="modifier_colis"),
    path('supprimer_colis/<int:id>/', supprimer_colis, name="supprimer_colis"),
    path('suivre_colis/', suivre_colis, name="suivre_colis"),
    path('deconnexion/', deconnexion, name="deconnexion"),

]
