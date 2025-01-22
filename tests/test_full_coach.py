def test_full_coach_success(test_client, create_test_user):
    """Test successful call to /api/full_coach."""
    # Create a test user
    user = create_test_user("premiumuser@example.com", "password123", role="premium")
    
    # Log in the user to get a token
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    token = login_response.json['access_token']

    # Make a valid full_coach request
    response = test_client.post('/api/full_coach', headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "weight": 150,
        "height_feet": 5,
        "height_inches": 10,
        "age": 25,
        "activity_factor": 1.55,
        "gender": "male"
    })

    # Assertions for a successful response
    assert response.status_code == 200
    assert "introduction" in response.json
    assert "stats" in response.json
    assert "advice" in response.json


def test_full_coach_missing_fields(test_client, create_test_user):
    """Test /api/full_coach with missing fields."""
    # Create a test user
    user = create_test_user("premiumuser@example.com", "password123", role="premium")
    
    # Log in the user to get a token
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    token = login_response.json['access_token']

    # Make a full_coach request with missing fields
    response = test_client.post('/api/full_coach', headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "weight": 150  # Missing required fields like height, age, activity_factor, etc.
    })

    # Assertions for a bad request
    assert response.status_code == 400
    assert "error" in response.json
    assert "Missing fields" in response.json['error']
    
def test_full_coach_access_denied(test_client, create_test_user):
    """Test that non-premium users are denied access to /api/full_coach."""
    # Create a free-tier user
    user = create_test_user("testuser@example.com", "password123", role="free")
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    token = login_response.json['access_token']

    # Attempt to access the premium endpoint
    response = test_client.post('/api/full_coach', headers={
        "Authorization": f"Bearer {token}"
    }, json={
        "weight": 150,
        "height_feet": 5,
        "height_inches": 10,
        "age": 25,
        "activity_factor": 1.55,
        "gender": "male"
    })

    assert response.status_code == 403
    assert "Access restricted" in response.json['error']