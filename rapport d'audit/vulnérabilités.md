# Ebauche des vulnérabilités identifiées

## Enumeration des vulnérabilités connues 

### SQLi

En effet, toutes les requêtes implémentées en dur ne sont pas préparés, ce qui implique que la partie dynamique de la requête sera interprétée si du code y est inséré.

Cette vulnérabilité est présente dans le fichier auth.py, dans les fonction :

 - register(): 
	A la ligne 41
```
    db.execute(
    	f'INSERT INTO user (username, password) VALUES '  #TODO : préparer la requête
    	f'("{username}", "{password}")'
    )
    db.commit()
    
   ```

 - login():
 - load_logged_in_user():
 - 
 
 **CORRIGE**
 
 ### Injection XSS
 ```<script>alert('XSS test')</script>```
 Dans le formulaire de création des posts
  **CORRIGE**
 
  Dans le formulaire de mise à jour des posts
 
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
