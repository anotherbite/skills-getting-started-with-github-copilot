import pytest
from fastapi.testclient import TestClient
from src.app import app  # Import de l'application FastAPI

client = TestClient(app)

def test_get_activities():
    """Test récupération de toutes les activités"""
    # Arrange: Aucune préparation nécessaire (données initiales déjà en place)
    
    # Act: Effectuer la requête GET
    response = client.get("/activities")
    
    # Assert: Vérifier la réponse
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data  # Vérifie qu'une activité existe
    assert "participants" in data["Chess Club"]

def test_signup_success():
    """Test inscription réussie à une activité"""
    # Arrange: Préparer les données (email et activité)
    email = "test@mergington.edu"
    activity = "Chess Club"
    
    # Act: Effectuer l'inscription
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Vérifier le succès et l'ajout
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    
    # Vérifier que l'étudiant est ajouté dans les données
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    """Test inscription en double (doit échouer)"""
    # Arrange: Inscrire une première fois
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Tenter une deuxième inscription
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Vérifier l'échec
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    """Test inscription à une activité inexistante"""
    # Arrange: Utiliser une activité invalide
    email = "test@mergington.edu"
    invalid_activity = "NonExistent"
    
    # Act: Tenter l'inscription
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert: Vérifier l'erreur 404
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    """Test désinscription réussie"""
    # Arrange: Inscrire l'étudiant d'abord
    email = "unregister@mergington.edu"
    activity = "Gym Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Effectuer la désinscription
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Vérifier le succès et la suppression
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    
    # Vérifier que l'étudiant est retiré
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity]["participants"]

def test_unregister_not_signed_up():
    """Test désinscription d'un étudiant non inscrit"""
    # Arrange: Utiliser un email non inscrit
    email = "notsigned@mergington.edu"
    activity = "Chess Club"
    
    # Act: Tenter la désinscription
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Vérifier l'erreur
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    """Test désinscription d'une activité inexistante"""
    # Arrange: Utiliser une activité invalide
    email = "test@mergington.edu"
    invalid_activity = "NonExistent"
    
    # Act: Tenter la désinscription
    response = client.delete(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert: Vérifier l'erreur 404
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]