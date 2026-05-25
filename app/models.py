from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100)
    code = models.CharField(max_length=100, default="")
    adresse = models.TextField()
    piece_identite = models.FileField(upload_to='pieces/')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_naissance = models.DateField(null=True)
    lieu_naissance = models.CharField(max_length=100, null=True)

class Succursale(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    adresse = models.TextField()

class Colis(models.Model):
    LISTE_ETATS = (
        ('traitement', 'En traitement'),
        ('voyage', 'En voyage'),
        ('arrive', 'Arrivée'), 
        ('annule', 'Annulé')
        )
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=100)
    description = models.TextField()
    destination = models.CharField(max_length=100)
    expediteur = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name="client_expediteur", null=True)
    recepteur = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name="client_recepteur", null=True)
    succursale = models.ForeignKey(Succursale, on_delete=models.SET_NULL, null=True)
    heure_depart = models.DateTimeField(null=True)
    heure_arrivee = models.DateTimeField(null=True)
    code = models.CharField(max_length=100, default="")
    etat = models.CharField(max_length=100, choices=LISTE_ETATS, default="traitement")
    est_valider = models.BooleanField(default=False)

class Tarif(models.Model):
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    montant = models.IntegerField()
    devise = models.CharField(max_length=100)

class Paiement(models.Model):
    montant = models.IntegerField()
    devise = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    date_paiement = models.DateTimeField()
    coli = models.ForeignKey(Colis, on_delete=models.RESTRICT)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)

