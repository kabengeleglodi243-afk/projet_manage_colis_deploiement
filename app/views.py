from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .models import Client, Succursale, Colis
from django.db.models import Q

# Récupération du modèle User par défaut de Django
User = get_user_model()

# Create your views here.

def connexion(request):
    """
    Vue de connexion des utilisateurs
    - Récupère les identifiants depuis le formulaire POST
    - Authentifie l'utilisateur
    - Redirige vers la liste des colis si succès
    - Affiche un message d'erreur si échec
    """
    # Récupération des données du formulaire
    username = request.POST.get('nom_utilisateur')
    password = request.POST.get('mot_de_passe')

    # Authentification de l'utilisateur
    user = authenticate(request, username = username, password = password)
    
    # Si l'authentification réussit
    if user:
        login(request, user)
        # Pas de message, redirection directe vers la liste des colis
        return redirect('lister_colis/')
    
    # Si l'authentification échoue (seulement si des identifiants ont été fournis)
    if username or password:
        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

    return render(request, 'authentication-login.html')

def register(request):
    """
    Vue d'inscription des nouveaux utilisateurs
    - Crée un compte utilisateur (User) et un profil client (Client)
    - Valide que les mots de passe correspondent
    - Vérifie l'unicité du nom d'utilisateur
    - Génère automatiquement un code client unique
    """
    import http.client
    import json

    conn = http.client.HTTPSConnection("restcountries.com")

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)",
    "Content-Type": "application/json" 
    }

    payload = json.dumps({
    "code": "CB",
    "name": "Rép du Congo"
    })

    conn.request("GET", "/v3.1/all?fields=name%2Ccapital%2Ccurrencies", payload, headersList)
    response = conn.getresponse()
    result = response.read()

    print(result.decode("utf-8"))

    


    if request.method == 'POST':
        # Récupération des données du formulaire d'inscription
        nom = request.POST.get('nom')
        postnom = request.POST.get('postnom')
        prenom = request.POST.get('prenom')
        mail = request.POST.get('mail')
        username = request.POST.get('nom_utilisateur')
        sexe = request.POST.get('sexe')
        adresse_physique = request.POST.get('adresse_physique')
        lieu = request.POST.get('lieu_naissance')
        date = request.POST.get('date_naissance')
        mot_de_passe_1 = request.POST.get('mot_de_passe_1')
        mot_de_passe_2 = request.POST.get('mot_de_passe_2')

        print(nom, postnom, prenom, mail, username, sexe, adresse_physique, lieu, date, mot_de_passe_1, mot_de_passe_2)

        # Validation: vérifier que les deux mots de passe sont identiques
        if mot_de_passe_1 != mot_de_passe_2:
            messages.error(request, "Les deux mots de passe doivent être identiques")
            return redirect("/register/")

        # Validation: vérifier que le nom d'utilisateur n'existe pas déjà
        if User.objects.filter(Q(username=username) | Q(email=mail)).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà")
            return redirect("/register/")
        
        # Création du compte utilisateur avec mot de passe hashé
        user = User.objects.create(
            username = username,
            email = mail,
            password = make_password(mot_de_passe_1),
        )

        # Création du profil client associé à l'utilisateur
        client = Client.objects.create(
            nom = nom,
            postnom = postnom,
            prenom = prenom,
            adresse = adresse_physique,
            lieu_naissance = lieu,
            date_naissance = date,
            user = user
        )
        # Génération du code client unique (format: PrenomNomUsername-ID)
        client.code = (prenom[0] + nom + username + "-" + str(client.id)).upper()
        client.save()

        # Message de succès avec le code client
        messages.success(request, f"Utilisateur créer avec succès. Votre code est : {client.code}")

        return redirect("/")

    # Affichage du formulaire d'inscription (méthode GET)
    return render(request, 'authentication-register.html')

@login_required
def enregistrer_colis(request):
    """
    Vue d'enregistrement d'un nouveau colis
    - Récupère les informations du colis depuis le formulaire
    - Associe l'expéditeur (utilisateur connecté) et le récepteur
    - Génère automatiquement un code colis unique
    - Redirige vers la liste des colis après création
    """
    # Récupération de toutes les succursales pour le formulaire
    succursales = Succursale.objects.all()

    if request.method == 'POST':
        # Récupération des données du formulaire
        description = request.POST.get('description')
        type = request.POST.get('type')
        poids = request.POST.get('poids')
        destination = request.POST.get('destination')
        succursale = request.POST.get('succursale')
        code_recepteur = request.POST.get('code_recepteur')

        print(description, type, poids, destination, succursale, code_recepteur)

        # Récupération des objets liés (expéditeur, succursale, récepteur)
        expediteur = Client.objects.get(user=request.user)  # L'expéditeur est l'utilisateur connecté
        succursale = Succursale.objects.get(id=succursale)
        recepteur = Client.objects.get(code=code_recepteur)  # Recherche du récepteur par son code
        
        # Création du colis dans la base de données
        colis = Colis.objects.create(
            description = description,
            type = type,
            poids = poids,
            destination = succursale.ville,  # La destination est la ville de la succursale
            succursale = succursale,
            recepteur = recepteur,
            expediteur = expediteur,
        )
        # Génération du code colis amélioré (format: COL-XXXX-YYYY)
        # XXXX: 4 premières lettres du type en majuscules
        # YYYY: ID du colis avec padding de 4 zéros
        type_prefix = type[:4].upper() if len(type) >= 4 else type.upper().ljust(4, 'X')
        colis.code = f"COL-{type_prefix}-{str(colis.id).zfill(4)}"
        colis.save()

        return redirect('/lister_colis/')

    # Affichage du formulaire d'enregistrement (méthode GET)
    return render(request, 'enregistrer-colis.html', {"succursales": succursales})

@login_required
def lister_colis(request):
    """
    Vue d'affichage de la liste des colis
    - Filtre les colis pour n'afficher que ceux de l'utilisateur connecté (en tant qu'expéditeur)
    - Affiche un tableau avec toutes les informations des colis
    """
    # Récupération des colis où l'utilisateur connecté est l'expéditeur
    colis = Colis.objects.filter(Q(expediteur__user=request.user) | Q(recepteur__user=request.user))
    
    return render(request, 'lister-colis.html', {"colis": colis})

@login_required
def detail_colis(request, id):
    """
    Vue d'affichage des détails d'un colis spécifique
    - Récupère le colis par son ID
    - Affiche toutes les informations détaillées (expéditeur, récepteur, succursale, etc.)
    """
    # Récupération du colis par son ID
    colis = Colis.objects.get(id=id)
    return render(request, 'detail-colis.html', {"colis": colis})

@login_required
def supprimer_colis(request, id):
    """
    Vue de suppression d'un colis
    - Récupère le colis par son ID
    - Supprime le colis de la base de données
    - Affiche un message de confirmation
    - Redirige vers la liste des colis
    """
    # Récupération du colis à supprimer
    colis = Colis.objects.get(id=id)
    # Suppression du colis
    colis.delete()
    messages.success(request, "Colis supprimé avec succès")
    return redirect('/lister_colis/')

@login_required
def modifier_colis(request, id):
    """
    Vue de modification d'un colis existant
    - Récupère le colis par son ID
    - Affiche un formulaire pré-rempli avec les données actuelles
    - Met à jour les informations du colis lors de la soumission
    - Redirige vers la liste des colis après modification
    """
    # Récupération du colis à modifier
    colis = Colis.objects.get(id=id)
    # Récupération de toutes les succursales pour le formulaire
    succursales = Succursale.objects.all()

    if request.method == 'POST':
        # Mise à jour des champs du colis avec les nouvelles valeurs
        colis.description = request.POST.get('description')
        colis.type = request.POST.get('type')
        colis.poids = request.POST.get('poids')
        succursale_id = request.POST.get('succursale')
        code_recepteur = request.POST.get('code_recepteur')

        # Mise à jour de la succursale et de la destination
        colis.succursale = Succursale.objects.get(id=succursale_id)
        colis.destination = colis.succursale.ville
        # Mise à jour du récepteur
        colis.recepteur = Client.objects.get(code=code_recepteur)
        # Sauvegarde des modifications
        colis.save()

        messages.success(request, "Colis modifié avec succès")
        return redirect('/lister_colis/')

    # Affichage du formulaire de modification (méthode GET)
    return render(request, 'modifier-colis.html', {"colis": colis, "succursales": succursales})

def suivre_colis(request):
    """
    Vue de suivi des colis
    - Affiche le formulaire de recherche de colis (GET)
    - Recherche un colis par son code et redirige vers la page de détail (POST)
    """
    message = None

    if request.method == 'POST':
        # Récupération du code du colis depuis le formulaire
        code_colis = request.POST.get('code_colis')
        
        try:
            # Recherche du colis par son code
            colis = Colis.objects.get(code=code_colis)
            # Redirection vers la page de détail du colis
            return redirect('detail_colis', id=colis.id)
        except Colis.DoesNotExist:
            # Message si le colis n'existe pas
            message = "Aucun colis trouvé avec ce code. Veuillez vérifier le code saisi."

    return render(request, 'suivre-colis.html', {"message": message})

@login_required
def deconnexion(request):
    """
    Vue de déconnexion des utilisateurs
    - Déconnecte l'utilisateur connecté
    - Redirige vers la page de connexion
    """
    from django.contrib.auth import logout
    # Déconnexion de l'utilisateur
    logout(request)
    return redirect('connexion')
