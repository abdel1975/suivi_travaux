
from django.contrib import admin
from .models import Projet, UserProfile

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('nom', 'province', 'commune', 'statut', 'taux_avancement')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'province')
    search_fields = ('user__username', 'province')


