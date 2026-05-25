from django.contrib import admin
from .models import Succursale, Client, Colis

# Register your models here.
@admin.register(Succursale)
class SuccursaleAdmin(admin.ModelAdmin):
    list_display = ("nom", "ville", "adresse")

@admin.register(Client)
class clientAdmin(admin.ModelAdmin):
    list_display = ("nom", "postnom", "prenom", "user", "code")

@admin.register(Colis)
class colisAdmin(admin.ModelAdmin):
    list_display = ("description", "type", "poids", "recepteur")
