def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_known_activity(client):
    response = client.get("/activities")
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    chess_club = body["Chess Club"]
    assert chess_club["description"]
    assert chess_club["schedule"]
    assert chess_club["max_participants"] == 12
    assert "michael@mergington.edu" in chess_club["participants"]


def test_signup_for_activity_success(client):
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_activity_duplicate_email(client):
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_unknown_activity(client):
    response = client.post("/activities/Not A Club/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_success(client):
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_student_not_signed_up(client):
    response = client.delete("/activities/Chess Club/participants/notsignedup@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_from_unknown_activity(client):
    response = client.delete("/activities/Not A Club/participants/someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
