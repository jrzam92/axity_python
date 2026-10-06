def test_create_order(client, auth_headers):
    """Test crear orden"""
    order_data = {
        "customer_name": "Juan Pérez",
        "product": "Laptop HP",
        "quantity": 2,
        "price": 15000.50,
        "status": "pending"
    }
    
    response = client.post(
        "/api/v1/orders/",
        json=order_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Juan Pérez"
    assert data["id"] is not None

def test_create_order_without_auth(client):
    """Test crear orden sin autenticación debe fallar"""
    response = client.post(
        "/api/v1/orders/",
        json={"customer_name": "Test", "product": "Test", "quantity": 1, "price": 100}
    )
    
    assert response.status_code == 403  # Forbidden

def test_list_orders(client, auth_headers):
    """Test listar órdenes"""
    # Crear orden primero
    client.post(
        "/api/v1/orders/",
        json={"customer_name": "Test", "product": "Test", "quantity": 1, "price": 100},
        headers=auth_headers
    )
    
    # Listar
    response = client.get("/api/v1/orders/", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "orders" in data
    assert len(data["orders"]) > 0

def test_update_order(client, auth_headers):
    """Test actualizar orden"""
    # Crear orden
    create_response = client.post(
        "/api/v1/orders/",
        json={"customer_name": "Test", "product": "Test", "quantity": 1, "price": 100},
        headers=auth_headers
    )
    order_id = create_response.json()["id"]
    
    # Actualizar
    response = client.put(
        f"/api/v1/orders/{order_id}",
        json={"status": "completed"},
        headers=auth_headers
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_delete_order(client, auth_headers):
    """Test eliminar orden"""
    # Crear orden
    create_response = client.post(
        "/api/v1/orders/",
        json={"customer_name": "Test", "product": "Test", "quantity": 1, "price": 100},
        headers=auth_headers
    )
    order_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/api/v1/orders/{order_id}", headers=auth_headers)
    
    assert response.status_code == 204
    
    # Verificar que ya no existe
    get_response = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert get_response.status_code == 404