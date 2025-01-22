def test_history_no_stats(test_client, create_test_user):
    """Test history endpoint with no stats."""
    user = create_test_user("premiumuser@example.com", "password123", role="premium")
    login_response = test_client.post('/api/login', json={
        "email": user.email,
        "password": "password123"
    })
    token = login_response.json['access_token']

    # Request history without any stats
    response = test_client.get('/api/history', headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 404  # Correctly expect 404 when no stats exist
    assert response.json['error'] == "No stats found for the user."



def test_history_with_stats(test_client, create_test_user):
    """Test history endpoint with existing stats."""
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
    db.session.commit()  # Commit the transaction immediately

    # Fetch history
    response = test_client.get('/api/history', headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert len(response.json['history']) == 1
