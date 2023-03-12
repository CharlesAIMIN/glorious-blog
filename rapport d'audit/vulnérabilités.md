# Ebauche des vulnérabilités identifiées

## Enumeration des vulnérabilités connues 

### SQLi

En effet, toutes les requêtes implémentées en dur ne sont pas préparés, ce qui implique que la partie dynamique de la requête sera interprétée si du code y est inséré.

Cette vulnérabilité est présente dans le fichier auth.py, dans les fonction :

 - register()
 - login()
 - load_logged_in_user()

Cette vulnérabilité est présente dans le fichier blog.py, dans les fonction :
 - login_required()
 - get_post()
 - login_required()
 - index()
 - create()
 
 **CORRIGE**
 
 ### Injection XSS
 ```<script>alert('XSS test')</script>```
 Dans le formulaire de création des posts
  **CORRIGE**
 
  Dans le formulaire de mise à jour des posts
   **CORRIGE**
 ### hash
 
 MDP non hashé dans la base
 
 
 **CORRIGE**
 
 ### anti bruteforce
 
 Pas d'anti brute force sur la page de connexion
 
   **CORRIGE**
 
 ### sanitization 
 
 Ajout regex, mdp au moins 8 caractères et escape sur les chanmps d'entrée dans login.html, register.html et auth.py
 
  **CORRIGE**
 
 ### Authentification failure
 
 Il est possible de changer la valeure "user_id" dans le cookie pour changer de session utilisateur
 
 # Axes d'amélioration 
 
 ## Page de profil
 
 Il peut être intéressant de rajouter une page de profil avec un avatar et la possibilité de changer son nom d'utilisateur
