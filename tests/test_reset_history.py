def test_reset_history_success(test_client, create_test_user):
    """Test successful reset of user history."""
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
    db.session.commit()  # Explicitly commit the transaction

    # Reset history
    response = test_client.delete('/api/reset_history', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json['message'] == "User stats deleted successfully."

    # Verify history is empty
    history_response = test_client.get('/api/history', headers={
        "Authorization": f"Bearer {token}"
    })
    assert history_response.status_code == 404
