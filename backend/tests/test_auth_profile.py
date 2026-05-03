from fastapi.testclient import TestClient


def test_login_and_profile_update(client: TestClient, auth_headers: dict[str, str]) -> None:
    profile_response = client.get("/api/profile", headers=auth_headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["skills"] == []

    update_response = client.put(
        "/api/profile",
        headers=auth_headers,
        json={
            "full_name": "AVKC",
            "target_role": "Python Engineer",
            "location": "Chicago",
            "experience_years": 5,
            "skills": ["Python", "FastAPI", "React", "Docker"],
            "preferences": {"remote": True},
        },
    )
    assert update_response.status_code == 200
    body = update_response.json()
    assert body["target_role"] == "Python Engineer"
    assert "FastAPI" in body["skills"]


def test_account_can_manage_multiple_profiles(client: TestClient, auth_headers: dict[str, str]) -> None:
    first_response = client.post(
        "/api/profiles",
        headers=auth_headers,
        json={
            "name": "Product Manager",
            "target_role": "Product Manager",
            "location": "Remote",
            "experience_years": 5,
            "skills": ["Product Strategy", "Roadmap"],
            "preferences": {},
        },
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/api/profiles",
        headers=auth_headers,
        json={
            "name": "System Architect",
            "target_role": "System Architect",
            "location": "Chicago",
            "experience_years": 8,
            "skills": ["Architecture", "Security", "Cloud"],
            "preferences": {},
        },
    )
    assert second_response.status_code == 201
    second_id = second_response.json()["id"]

    activate_response = client.post(f"/api/profiles/{second_id}/activate", headers=auth_headers)
    assert activate_response.status_code == 200
    assert activate_response.json()["is_active"] is True

    profiles_response = client.get("/api/profiles", headers=auth_headers)
    assert profiles_response.status_code == 200
    profiles = profiles_response.json()
    assert len(profiles) == 2
    assert sum(1 for profile in profiles if profile["is_active"]) == 1
    assert profiles[0]["name"] == "System Architect"
