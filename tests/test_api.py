import pytest

@pytest.mark.asyncio
async def test_ingest_match_success(async_client):
    test_match_id = 7500000000
    response = await async_client.get(f"/api/v1/match/{test_match_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["match_id"] == test_match_id
    assert data["radiant_win"] is True
    assert data["patch"] == 734

@pytest.mark.asyncio
async def test_ingest_match_invalid_id_type(async_client):
    response = await async_client.get("/api/v1/match/not_an_integer")
    assert response.status_code == 422