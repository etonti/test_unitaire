# Mini gestionnaire de tâches en ligne de commande
# Permet d'ajouter, lister, modifier et supprimer des tâches


# Importation des modules nécessaires
import json      # Pour la gestion des fichiers JSON
import os        # Pour les opérations sur le système de fichiers
from typing import List, Dict, Optional  # Pour les annotations de type

# Type personnalisé pour une tâche
Tache = Dict[str, str]

class GestionnaireTaches:
    # Classe principale pour gérer les opérations sur les tâches
    
    def __init__(self, chemin_fichier: str = "taches.json"):
        # """
        # Initialise le gestionnaire de tâches.
        
        # Args:
        #     chemin_fichier (str): Chemin vers le fichier de stockage. 
        #                          Par défaut: "taches.json"
        # """
        self.chemin_fichier = chemin_fichier  # Chemin du fichier de sauvegarde
        self.liste_taches: List[Tache] = []   # Liste pour stocker les tâches
        self.charger_taches()                # Charge les tâches existantes
    
    def charger_taches(self) -> None:
        """Charge les tâches depuis le fichier JSON"""
        # Vérifie si le fichier existe
        if os.path.exists(self.chemin_fichier):
            # Ouvre le fichier en lecture
            with open(self.chemin_fichier, 'r', encoding='utf-8') as fichier:
                try:
                    # Charge le contenu JSON
                    self.liste_taches = json.load(fichier)
                except json.JSONDecodeError:
                    # Si le fichier est corrompu, initialise une liste vide
                    self.liste_taches = []
        else:
            # Si le fichier n'existe pas, initialise une liste vide
            self.liste_taches = []
    
    def sauvegarder_taches(self) -> None:
        """Sauvegarde les tâches dans le fichier JSON"""
        # Ouvre le fichier en écriture
        with open(self.chemin_fichier, 'w', encoding='utf-8') as fichier:
            # Écrit les tâches dans le fichier
            json.dump(self.liste_taches, fichier, indent=4)
    
    def ajouter_tache(self, description: str) -> None :
        """
        Ajoute une nouvelle tâche à la liste.
        
        Args:
            description (str): Description de la tâche
            
        Raises:
            ValueError: Si la description est vide
        """
        # Vérifie que la description n'est pas vide
        if not description.strip():
            raise ValueError("La description ne peut pas être vide")
            
        # Crée une nouvelle tâche
        nouvelle_tache: Tache = {
            "id": str(len(self.liste_taches) + 1),  # ID auto-incrémenté
            "description": description.strip(),      # Description nettoyée
            "statut": "à faire"                     # Statut par défaut
        }
        # Ajoute la tâche à la liste
        self.liste_taches.append(nouvelle_tache)
        # Sauvegarde les modifications
        self.sauvegarder_taches()
    
    def lister_taches(self, filtre_statut: Optional[str] = None) -> List[Tache]:
        """
        Retourne la liste des tâches, avec option de filtrage.
        
        Args:
            filtre_statut (str, optional): Statut pour filtrer (ex: "à faire")
                                          
        Returns:
            List[Tache]: Liste des tâches filtrées ou complète
        """
        # Si un filtre est spécifié
        if filtre_statut:
            # Retourne les tâches correspondant au statut
            return [tache for tache in self.liste_taches 
                    if tache["statut"] == filtre_statut]
        # Sinon retourne toutes les tâches
        return self.liste_taches
    
    def marquer_comme_terminee(self, id_tache: str) -> None:
        """
        Marque une tâche comme terminée.
        
        Args:
            id_tache (str): ID de la tâche à marquer
            
        Raises:
            ValueError: Si l'ID n'existe pas
        """
        # Parcourt toutes les tâches
        for tache in self.liste_taches:
            if tache["id"] == id_tache:
                # Modifie le statut
                tache["statut"] = "terminée"
                self.sauvegarder_taches()
                return
        # Si la tâche n'est pas trouvée
        raise ValueError(f"Tâche avec l'ID {id_tache} non trouvée")
    
    def supprimer_tache(self, id_tache: str) -> None:
        """
        Supprime une tâche de la liste.
        
        Args:
            id_tache (str): ID de la tâche à supprimer
            
        Raises:
            ValueError: Si l'ID n'existe pas
        """
        # Garde la longueur initiale pour vérification
        longueur_initiale = len(self.liste_taches)
        # Filtre les tâches pour exclure celle à supprimer
        self.liste_taches = [tache for tache in self.liste_taches 
                            if tache["id"] != id_tache]
        
        # Vérifie si une tâche a été supprimée
        if len(self.liste_taches) == longueur_initiale:
            raise ValueError(f"Tâche avec l'ID {id_tache} non trouvée")
        
        # Sauvegarde les modifications
        self.sauvegarder_taches()
    
    def modifier_tache(self, id_tache: str, nouvelle_description: str) -> None:
        """
        Modifie la description d'une tâche.
        
        Args:
            id_tache (str): ID de la tâche à modifier
            nouvelle_description (str): Nouvelle description
            
        Raises:
            ValueError: Si l'ID n'existe pas ou description vide
        """
        # Parcourt toutes les tâches
        for tache in self.liste_taches:
            if tache["id"] == id_tache:
                # Vérifie la nouvelle description
                if not nouvelle_description.strip():
                    raise ValueError("La description ne peut pas être vide")
                # Modifie la description
                tache["description"] = nouvelle_description.strip()
                self.sauvegarder_taches()
                return
        # Si la tâche n'est pas trouvée
        raise ValueError(f"Tâche avec l'ID {id_tache} non trouvée")


def afficher_menu() -> None:
    """Affiche le menu des options disponibles"""
    print("\n=== Gestionnaire de Tâches ===")
    print("1. Ajouter une tâche")
    print("2. Lister toutes les tâches")
    print("3. Lister les tâches à faire")
    print("4. Lister les tâches terminées")
    print("5. Marquer une tâche comme terminée")
    print("6. Supprimer une tâche")
    print("7. Modifier une tâche")
    print("8. Quitter")


def main() -> None:
    """Fonction principale pour l'interface utilisateur"""
    gestionnaire = GestionnaireTaches()
    
    while True:
        afficher_menu()
        choix = input("\nChoisissez une option (1-8): ")
        
        try:
            if choix == "1":
                description = input("Description de la tâche: ")
                gestionnaire.ajouter_tache(description)
                print("Tâche ajoutée avec succès!")
            
            elif choix == "2":
                taches = gestionnaire.lister_taches()
                print("\n=== Toutes les Tâches ===")
                for tache in taches:
                    print(f"{tache['id']}. [{tache['statut']}] {tache['description']}")
            
            elif choix == "3":
                taches = gestionnaire.lister_taches("à faire")
                print("\n=== Tâches à Faire ===")
                for tache in taches:
                    print(f"{tache['id']}. {tache['description']}")
            
            elif choix == "4":
                taches = gestionnaire.lister_taches("terminée")
                print("\n=== Tâches Terminées ===")
                for tache in taches:
                    print(f"{tache['id']}. {tache['description']}")
            
            elif choix == "5":
                id_tache = input("ID de la tâche à marquer comme terminée: ")
                gestionnaire.marquer_comme_terminee(id_tache)
                print("Tâche marquée comme terminée!")
            
            elif choix == "6":
                id_tache = input("ID de la tâche à supprimer: ")
                gestionnaire.supprimer_tache(id_tache)
                print("Tâche supprimée avec succès!")
            
            elif choix == "7":
                id_tache = input("ID de la tâche à modifier: ")
                nouvelle_description = input("Nouvelle description: ")
                gestionnaire.modifier_tache(id_tache, nouvelle_description)
                print("Tâche modifiée avec succès!")
            
            elif choix == "8":
                print("Au revoir!")
                break
            
            else:
                print("Option invalide. Veuillez choisir un nombre entre 1 et 8.")
        
        except ValueError as e:
            print(f"Erreur: {e}")


if __name__ == "__main__":
    main()