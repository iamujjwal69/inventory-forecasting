import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        res = await ac.post("/api/auth/register", json={
            "name": "testuser",
            "email": "test@example.com",
            "password": "testpass"
        })
        assert res.status_code == 200
        token = res.json()["access_token"]
        # Login
        res2 = await ac.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "testpass"
        })
        assert res2.status_code == 200
        # Test protected route
        headers = {"Authorization": f"Bearer {token}"}
        res3 = await ac.get("/api/products", headers=headers)
        assert res3.status_code == 200
