from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Projet
import json
import pandas as pd
from django.http import HttpResponse
from django import forms
from django.shortcuts import render, get_object_or_404
from django.contrib import messages





@login_required
def dashboard(request):
    user = request.user
    user_profile = user.userprofile
    selected_province = None

    # 🔹 Cas provincial
    if user_profile.role == 'provincial':
        projets = Projet.objects.filter(province=user_profile.province)
    else:
        provinces = Projet.objects.values_list('province', flat=True).distinct().order_by('province')
        selected_province = request.GET.get('province')
        if selected_province:
            projets = Projet.objects.filter(province=selected_province)
        else:
            projets = Projet.objects.all()

    # 🔢 Statistiques
    total = projets.count()
    en_cours = projets.filter(situation='en_cours').count()
    acheve = projets.filter(situation='acheve').count()
    en_arret = projets.filter(situation='en_arret').count()

    # 🗺️ Données carte (⚠️ Assure-toi que ces champs existent)
    projets_data = projets.values(
        'intitule', 'province', 'commune',
        'latitude', 'longitude', 'situation'
    )
    print(list(projets.values('intitule', 'latitude', 'longitude', 'situation')))

    context = {
        'user': user,
        'user_profile': user_profile,
        'total': total,
        'en_cours': en_cours,
        'termine': acheve,     # Pour compatibilité avec le template
        'en_retard': en_arret, # idem
        'projets_json': json.dumps(list(projets_data)),
        'selected_province': selected_province,
    }

    if user_profile.role == 'regional':
        context['provinces'] = provinces

    return render(request, 'projets/dashboard.html', context)

from django.shortcuts import render, redirect
from .forms import ProjetForm
from django.contrib.auth.decorators import login_required



@login_required
def ajouter_projet(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)

            # 🔒 Si utilisateur provincial → on force sa province et on ne lui laisse pas choisir
            if user_profile.role == 'provincial':
                projet.province = user_profile.province

            projet.save()
            return redirect('dashboard')
    else:
        form = ProjetForm()

        # Astuce UX: Pré-remplir la province (readonly côté provincial)
        if user_profile.role == 'provincial':
            form.fields['province'].widget = forms.TextInput(attrs={'readonly': 'readonly'})
            form.initial['province'] = user_profile.province

    return render(request, 'projets/ajouter_projet.html', {'form': form})



@login_required
def export_excel(request, filtre):
    user_profile = request.user.userprofile

    # 🔹 Filtrage par rôle utilisateur
    if user_profile.role == 'provincial':
        projets = Projet.objects.filter(province=user_profile.province)
    else:
        projets = Projet.objects.all()

    # 🔹 Filtrage selon la situation du projet
    if filtre == 'en_cours':
        projets = projets.filter(situation='en_cours')
    elif filtre == 'acheve':
        projets = projets.filter(situation='acheve')
    elif filtre == 'en_arret':
        projets = projets.filter(situation='en_arret')
    # sinon 'tous' → aucun filtre

    # 🔹 Conversion en DataFrame Pandas
    df = pd.DataFrame(list(projets.values(
        'intitule', 'province', 'commune',
        'topographe', 'etude_geotechnique', 'architecte',
        'etude_technique', 'control_technique', 'delai_execution',
        'date_debut', 'date_fin_prevue', 'situation'
    )))

    # 🔹 Préparation de la réponse HTTP
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="projets_{filtre}.xlsx"'

    # 🔹 Exportation du fichier Excel
    df.to_excel(response, index=False, sheet_name='Projets')

    return response

@login_required
def liste_suivi_projets(request):
    user_profile = request.user.userprofile
    if user_profile.role == 'provincial':
        projets = Projet.objects.filter(province=user_profile.province)
    else:
        projets = Projet.objects.all()

    return render(request, 'projets/liste_suivi_projets.html', {'projets': projets})

@login_required
def suivi_execution(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    # On mettra le formulaire complet ici après
    return render(request, 'projets/suivi_execution_detail.html', {'projet': projet})

from .models import SuiviExecution

@login_required
def suivi_detail(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)

    if request.method == 'POST':
        data = request.POST
        SuiviExecution.objects.create(
            projet=projet,
            topo_date_debut=data.get('topo_date_debut'),
            topo_date_fin=data.get('topo_date_fin'),
            topo_montant=data.get('topo_montant'),
            geo_date_debut=data.get('geo_date_debut'),
            geo_date_fin=data.get('geo_date_fin'),
            geo_montant=data.get('geo_montant'),
            archi_date_debut=data.get('archi_date_debut'),
            archi_date_fin=data.get('archi_date_fin'),
            archi_montant=data.get('archi_montant'),
            etud_date_debut=data.get('etud_date_debut'),
            etud_date_fin=data.get('etud_date_fin'),
            etud_montant=data.get('etud_montant'),
            ctrl_date_debut=data.get('ctrl_date_debut'),
            ctrl_date_fin=data.get('ctrl_date_fin'),
            ctrl_montant=data.get('ctrl_montant'),
            trav_date_debut=data.get('trav_date_debut'),
            trav_date_fin=data.get('trav_date_fin'),
            trav_montant=data.get('trav_montant'),
            date_arret=data.get('date_arret'),
            taux_avancement=data.get('taux_avancement') or 0,
            taux_paiement=data.get('taux_paiement') or 0,
        )
        messages.success(request, "Suivi enregistré avec succès ✅")
        return redirect('liste_suivi_projets')

    return render(request, 'projets/suivi_execution_detail.html', {'projet': projet})

@login_required
def liste_suivi_projets(request):
    user_profile = request.user.userprofile

    # 🔹 Si l’utilisateur est provincial → il ne voit que les projets de sa province
    if user_profile.role == 'provincial':
        projets = Projet.objects.filter(province=user_profile.province)
    else:
        projets = Projet.objects.all()

    context = {
        'projets': projets,
        'user_profile': user_profile,
    }
    return render(request, 'projets/liste_suivi_projets.html', context)

@login_required
def projet_detail(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    return render(request, 'projets/projet_detail.html', {'projet': projet})

@login_required
def projet_edit(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)

    if request.method == 'POST':
        projet.intitule = request.POST.get('intitule')
        projet.commune = request.POST.get('commune')
        projet.topographe = request.POST.get('topographe')
        projet.etude_geotechnique = request.POST.get('etude_geotechnique')
        projet.architecte = request.POST.get('architecte')
        projet.etude_technique = request.POST.get('etude_technique')
        projet.control_technique = request.POST.get('control_technique')
        projet.delai_execution = request.POST.get('delai_execution')
        projet.date_debut = request.POST.get('date_debut')
        projet.date_fin_prevue = request.POST.get('date_fin_prevue')
        projet.situation = request.POST.get('situation')

        # Province fixée automatiquement pour les utilisateurs provinciaux
        if request.user.userprofile.role == 'provincial':
            projet.province = request.user.userprofile.province
        else:
            projet.province = request.POST.get('province')

        projet.save()
        messages.success(request, "✅ Projet modifié avec succès !")
        return redirect('liste_suivi_projets')

    return render(request, 'projets/projet_edit.html', {'projet': projet})





@login_required
def projet_delete(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    if request.method == 'POST':
        projet.delete()
        messages.success(request, f"✅ Le projet « {projet.intitule} » a bien été supprimé.")
        return redirect('liste_suivi_projets')
    return render(request, 'projets/projet_delete_confirm.html', {'projet': projet})



