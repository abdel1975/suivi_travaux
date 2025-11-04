from django import forms
from .models import Projet

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = [
            'intitule', 'province', 'commune',
            'topographe', 'etude_geotechnique', 'architecte',
            'etude_technique', 'control_technique', 'delai_execution',
            'date_debut', 'date_fin_prevue', 'situation',
            'latitude', 'longitude',
        ]
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin_prevue': forms.DateInput(attrs={'type': 'date'}),
        }

