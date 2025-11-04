from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # racine -> login
    path('', RedirectView.as_view(url='/login/', permanent=False)),

    # pages existantes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ajouter/', views.ajouter_projet, name='ajouter_projet'),

    # ✅ nouvelles routes de suivi
    path('suivi/', views.liste_suivi_projets, name='liste_suivi_projets'),
    path('suivi/<int:projet_id>/', views.suivi_execution, name='suivi_execution'),
    path('export/<str:filtre>/', views.export_excel, name='export_excel'),
    path('suivi/<int:projet_id>/', views.suivi_detail, name='suivi_detail'),
    path('suivi_projets/', views.liste_suivi_projets, name='liste_suivi_projets'),
    path('suivi/<int:projet_id>/', views.suivi_detail, name='suivi_detail'),
    path('projet/<int:projet_id>/', views.projet_detail, name='projet_detail'),
    path('projet/<int:projet_id>/modifier/', views.projet_edit, name='projet_edit'),
    path('projet/<int:projet_id>/supprimer/', views.projet_delete, name='projet_delete'),



]

