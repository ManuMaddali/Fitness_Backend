def test_coach_access_free_user(test_client, create_test_user):
    """Test that free users can access /api/coach with a valid token."""
    # Create a free user
    user = create_test_user("freeuser@example.com", "password123", role="free")

    # Log in to retrieve the token
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })

    # Debugging: Ensure token is retrieved
    print(f"Login Response: {login_response.json}")
    assert login_response.status_code == 200, "Login failed"
    token = login_response.json['access_token']
    assert token, "No token returned from login"

    # Make a request to the /api/coach endpoint
    response = test_client.post('/api/coach', headers={
        "Authorization": f"Bearer {token}"  # Add the token here
    }, json={"query": "What is a good workout?"})

    # Debug response
    print(f"Coach Endpoint Response: {response.json}")
    assert response.status_code == 200
    assert "message" in response.json


def test_coach_access_premium_user(test_client, create_test_user):
    """Test that premium users can access /api/coach with a valid token."""
    # Create a premium user
    user = create_test_user("premiumuser@example.com", "password123", role="premium")
    
    # Verify the user's role
    assert user.id is not None, "User ID should not be None after creation."
    assert user.role == "premium", f"Expected role to be 'premium', but got '{user.role}'"

    # Log in and retrieve the token
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    
    # Debugging: Print the login response
    print(f"Login Response: {login_response.json}")
    assert login_response.status_code == 200, "Login failed"
    token = login_response.json.get('access_token')
    assert token, "No token returned from login"

    # Access the /api/coach endpoint
    response = test_client.post('/api/coach', headers={
        "Authorization": f"Bearer {token}"
    }, json={"query": "What is a good workout?"})

    # Debug response
    print(f"Coach Endpoint Response: {response.json}")
    assert response.status_code == 200
    assert "message" in response.json


def test_coach_behavior_based_response(test_client, create_test_user):
    """Test that the /api/coach endpoint includes past queries in its responses."""
    # Create a premium user
    user = create_test_user("premiumuser@example.com", "password123", role="premium")

    # Log in to retrieve the token
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    token = login_response.json['access_token']

    # Add a past interaction
    from models import UserInteractions, db
    interaction = UserInteractions(
        user_id=user.id,
        query="How can I lose weight?",
        response="Eat fewer calories and exercise more."
    )
    db.session.add(interaction)
    db.session.commit()

    # Debug: Check database state
    interactions = UserInteractions.query.filter_by(user_id=user.id).all()
    print(f"User Interactions in DB: {interactions}")

    # Access the /api/coach endpoint
    response = test_client.post('/api/coach', headers={
        "Authorization": f"Bearer {token}"
    }, json={"query": "What is the best workout for weight loss?"})

    # Debug response
    print(f"Coach Endpoint Response: {response.json}")
    assert response.status_code == 200
    assert "Past Interaction" in response.json


def test_coach_personalized_and_categorized_response(test_client, create_test_user):
    """Test personalized and categorized responses from /api/coach."""
    # Create a premium user
    user = create_test_user("premiumuser@example.com", "password123", role="premium")
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    token = login_response.json['access_token']

    # Add mock stats to the database
    from models import UserStats, db
    stat = UserStats(
        user_id=user.id,
        tdee=2500,
        bmi=22.5,
        bfp=15.0,
        bmr=1600,
        ibw=70,
        hydration=2.5
    )
    db.session.add(stat)
    db.session.commit()

    # Debug: Check database state
    stats = UserStats.query.filter_by(user_id=user.id).all()
    print(f"User Stats in DB: {stats}")

    # Access the /api/coach endpoint
    response = test_client.post('/api/coach', headers={
        "Authorization": f"Bearer {token}"
    }, json={"query": "What is a healthy diet?"})

    # Debug response
    print(f"Coach Endpoint Response: {response.json}")
    assert response.status_code == 200
    assert "Your stats: TDEE is 2500 calories/day" in response.json['message']
    assert "nutrition coach" in response.json['message'].lower()
