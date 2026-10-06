def test_login_success(client):
    """Test login exitoso"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """Test login con credenciales inválidas"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"}
    )
    
    assert response.status_code == 401