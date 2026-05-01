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
