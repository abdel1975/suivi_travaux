from django.db import models
from django.contrib.auth.models import User

class Projet(models.Model):
    SITUATION_CHOICES = [
        ('en_cours', 'En Cours'),
        ('acheve', 'Achevé'),
        ('en_arret', 'En Arrêt'),
    ]

    # ✅ Nouveaux champs
    intitule = models.CharField("Intitulé du Projet", max_length=255)
    province = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    topographe = models.CharField("Topographe", max_length=150, blank=True, null=True)
    etude_geotechnique = models.CharField("Étude Géotechnique", max_length=150, blank=True, null=True)
    architecte = models.CharField("Architecte", max_length=150, blank=True, null=True)
    etude_technique = models.CharField("Étude Technique", max_length=150, blank=True, null=True)
    control_technique = models.CharField("Contrôle Technique", max_length=150, blank=True, null=True)
    delai_execution = models.CharField("Délai d’Exécution", max_length=100, blank=True, null=True)
    date_debut = models.DateField("Date de Début")
    date_fin_prevue = models.DateField("Date de Fin Prévue")
    situation = models.CharField("Situation", max_length=20, choices=SITUATION_CHOICES, default='en_cours')

    # 📍 Coordonnées (déjà utilisées par ta carte)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    # 🧩 Compat : on garde TEMPORAIREMENT les anciens champs pour éviter les gros diffs DB
    # (non utilisés dans le formulaire ; on pourra les supprimer plus tard)
    nom = models.CharField(max_length=200, blank=True, null=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    taux_avancement = models.IntegerField(default=0, blank=True, null=True)
    statut = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.intitule or self.nom or "Projet"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('regional', 'Utilisateur régional'),
        ('provincial', 'Utilisateur provincial'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='provincial',  # ✅ bien placé ici
    )
    province = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role}) - {self.province or '---'}"

class SuiviExecution(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='suivis')

    # Topographe
    topo_date_debut = models.DateField(blank=True, null=True)
    topo_date_fin = models.DateField(blank=True, null=True)
    topo_montant = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Étude géotechnique
    geo_date_debut = models.DateField(blank=True, null=True)
    geo_date_fin = models.DateField(blank=True, null=True)
    geo_montant = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Architecte
    archi_date_debut = models.DateField(blank=True, null=True)
    archi_date_fin = models.DateField(blank=True, null=True)
    archi_montant = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Étude technique
    etud_date_debut = models.DateField(blank=True, null=True)
    etud_date_fin = models.DateField(blank=True, null=True)
    etud_montant = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Contrôle technique
    ctrl_date_debut = models.DateField(blank=True, null=True)
    ctrl_date_fin = models.DateField(blank=True, null=True)
    ctrl_montant = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Travaux de construction
    trav_date_debut = models.DateField(blank=True, null=True)
    trav_date_fin = models.DateField(blank=True, null=True)
    trav_montant = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Autres informations
    date_arret = models.DateField(blank=True, null=True)
    taux_avancement = models.PositiveIntegerField(default=0)
    taux_paiement = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Suivi du projet {self.projet.intitule}"

