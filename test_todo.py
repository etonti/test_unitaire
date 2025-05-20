"""
Tests unitaires pour le gestionnaire de tâches
"""
import os
import pytest
import tempfile
from todo import GestionnaireTaches

@pytest.fixture
def fichier_temporaire():
    """Crée un fichier temporaire pour les tests"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
        yield f.name
    os.unlink(f.name)

def test_ajouter_tache(fichier_temporaire):
    """Teste l'ajout d'une tâche"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    gestionnaire.ajouter_tache("Test tâche")
    assert len(gestionnaire.liste_taches) == 1
    assert gestionnaire.liste_taches[0]["description"] == "Test tâche"
    assert gestionnaire.liste_taches[0]["statut"] == "à faire"

def test_ajouter_tache_vide(fichier_temporaire):
    """Teste qu'on ne peut pas ajouter une tâche vide"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    with pytest.raises(ValueError):
        gestionnaire.ajouter_tache("")

def test_marquer_comme_terminee(fichier_temporaire):
    """Teste le marquage d'une tâche comme terminée"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    gestionnaire.ajouter_tache("Test tâche")
    gestionnaire.marquer_comme_terminee("1")
    assert gestionnaire.liste_taches[0]["statut"] == "terminée"

def test_marquer_tache_inexistante(fichier_temporaire):
    """Teste qu'on ne peut pas marquer une tâche inexistante"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    with pytest.raises(ValueError):
        gestionnaire.marquer_comme_terminee("999")

def test_supprimer_tache(fichier_temporaire):
    """Teste la suppression d'une tâche"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    gestionnaire.ajouter_tache("Test tâche")
    gestionnaire.supprimer_tache("1")
    assert len(gestionnaire.liste_taches) == 0

def test_supprimer_tache_inexistante(fichier_temporaire):
    """Teste qu'on ne peut pas supprimer une tâche inexistante"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    with pytest.raises(ValueError):
        gestionnaire.supprimer_tache("999")

def test_modifier_tache(fichier_temporaire):
    """Teste la modification d'une tâche"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    gestionnaire.ajouter_tache("Test tâche")
    gestionnaire.modifier_tache("1", "Nouvelle description")
    assert gestionnaire.liste_taches[0]["description"] == "Nouvelle description"

def test_modifier_tache_description_vide(fichier_temporaire):
    """Teste qu'on ne peut pas mettre une description vide"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    gestionnaire.ajouter_tache("Test tâche")
    with pytest.raises(ValueError):
        gestionnaire.modifier_tache("1", "")

def test_lister_taches_filtre(fichier_temporaire):
    """Teste le filtrage des tâches"""
    gestionnaire = GestionnaireTaches(fichier_temporaire)
    gestionnaire.ajouter_tache("Tâche 1")
    gestionnaire.ajouter_tache("Tâche 2")
    gestionnaire.marquer_comme_terminee("1")
    
    taches_a_faire = gestionnaire.lister_taches("à faire")
    taches_terminees = gestionnaire.lister_taches("terminée")
    
    assert len(taches_a_faire) == 1
    assert len(taches_terminees) == 1
    assert taches_a_faire[0]["description"] == "Tâche 2"
    assert taches_terminees[0]["description"] == "Tâche 1"