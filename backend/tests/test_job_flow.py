from fastapi.testclient import TestClient


def test_source_scan_creates_scored_jobs(client: TestClient, auth_headers: dict[str, str]) -> None:
    client.put(
        "/api/profile",
        headers=auth_headers,
        json={
            "full_name": "AVKC",
            "target_role": "Engineer",
            "location": "Remote",
            "experience_years": 5,
            "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
            "preferences": {},
        },
    )

    source_response = client.post(
        "/api/sources",
        headers=auth_headers,
        json={
            "name": "Mock Source",
            "url": "https://example.com/search/python",
            "source_type": "mock",
            "enabled": True,
            "scan_interval_minutes": 5,
        },
    )
    assert source_response.status_code == 201
    source_id = source_response.json()["id"]

    scan_response = client.post(f"/api/sources/{source_id}/scan", headers=auth_headers)
    assert scan_response.status_code == 200
    assert scan_response.json()["created"] == 2

    jobs_response = client.get("/api/jobs?min_score=50", headers=auth_headers)
    assert jobs_response.status_code == 200
    jobs = jobs_response.json()
    assert len(jobs) >= 1
    assert jobs[0]["score"] >= 50
