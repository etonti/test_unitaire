#je dois créer ujn mini gestionnaire de tache en ligne de commande
#il va permettre d'ajouter, lister, modifier et supprimer des taches

#je vais importer les modules nécessaires
import json      # Pour la gestion des fichiers JSON
import os        # Pour les opérations sur le système de fichiers
from typing import List, Dict, Optional  # Pour les annotations de type

#Pour les taches, je crée un type personnalisé
Tache = Dict[str,str]

#Maintenant je crée ma classe principale ou tout va se passer (toutes les opérations sur les tâches)
class GestionnaireTaches:
    #je vais intialiser ensuite le gestionnaire de taches,*
    #je passe en paramètres le chemin du fichier contenant les tâches
    
    def __init___(self, chemin_fichier: str = "taches.json"):
        self.cheminfichier = cheminfichier 
        self.listTaches : List[Tache] =[]
        self.chargerTaches() #méthode pour charger les taches
        
    def chargerTaches(self) -> None:
        if os.path.exists(self.cheminfichier):
            with open (self.cheminfichier, "r", encoding="utf-8"):
                try:
                    self.liste_taches = json.load(fichier)
                except json.JSONDecodeError:
                    # Si le fichier est corrompu, initialise une liste vide
                    self.liste_taches = []
        else:
            #inititalise une liste vide sinon
            self.liste_taches = []
            
    def sauvegarderTaches(self)->None:
        #on va sauvegarder les taches dans le fichier json
         with open (self.cheminfichier, "w",encoding="utf-8") as fichier:
             json.dump(self.liste_taches, fichier, indent=4)
             
    
    def ajouterTaches(self, description : str)->None:
        #on vérifie que la description n'est pas vide
        if not description.strip():
            raise ValueError("La description ne peut pas être vide")
        
        #on crée ensuite une nouvelle tache
        nouvelleTache : Tache = {
            "id":str(len(self.liste_taches)+1), #ici j'auto incrémente l'ID
            "description": description.strip(),
            "statut": "a faire" 
        }
        
        #tout est bon, maintenant on ajoute la tache à la liste
        self.liste_taches.append(nouvelleTache)
        self.sauvegarder_taches()
            
    def listerTaches(self, filtre_statut: Optional[str] = None)->List[Tache]:
        if(filtre_statut):
            return [tache for tache in self.liste_Taches
            if(tache["statut"] == filtre_statut) ]
            
        return self.liste.taches
    
    def marquer_comme_terminee(self, id_tache : str):
        for tache in self.liste_taches:
            if tache["id"] == id_tache:
                # Modifie le statut
                tache["statut"] = "terminée"
                self.sauvegarder_taches()
                return
            
    def supprimer_taches(self,)
        
                
                   