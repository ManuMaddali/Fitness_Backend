def test_register(test_client):
    """Test user registration."""
    response = test_client.post('/api/register', json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully."

def test_register_success(test_client):
    """Test successful user registration."""
    response = test_client.post('/api/register', json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully."

def test_register_existing_user(test_client, create_test_user):
    """Test registering a user with an existing email."""
    create_test_user("testuser@example.com", "password123")
    response = test_client.post('/api/register', json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json['error'] == "User with this email already exists."

def test_login_success(test_client, create_test_user):
    """Test successful user login."""
    create_test_user("testuser@example.com", "password123")
    response = test_client.post('/api/login', json={
        "email": "testuser@example.com",
        "password": "password123"
    })
    print(f"Login Response: {response.json}")  # Debugging
    assert response.status_code == 200
    assert "access_token" in response.json

def test_login_invalid_credentials(test_client, create_test_user):
    """Test login with invalid credentials."""
    create_test_user("testuser@example.com", "password123")
    response = test_client.post('/api/login', json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    print(f"Login Response: {response.json}")  # Debugging
    assert response.status_code == 401
    assert response.json['error'] == "Invalid email or password."

def test_login_nonexistent_user(test_client):
    """Test login for a user that does not exist."""
    response = test_client.post('/api/login', json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })
    assert response.status_code == 401  # Corrected from 404
    assert response.json['error'] == "Invalid email or password."


def test_login(test_client, create_test_user):
    """Test user login."""
    create_test_user("testuser@example.com", "testpassword")
    response = test_client.post('/api/login', json={
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    print(f"Login Response: {response.json}")  # Debugging
    assert response.status_code == 200
    assert "access_token" in response.json