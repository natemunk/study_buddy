from httpx import AsyncClient
import sys
sys.path.append("../../app")
from app.main import app  # Import the FastAPI app instance


async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
