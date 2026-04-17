import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.api.dependencies import get_opendota_client, get_mlflow_tracker
from app.models.schemas import MatchData

class MockOpenDotaClient:
    async def fetch_match(self, match_id: int) -> MatchData:
        return MatchData(
            match_id=match_id,
            radiant_win=True,
            duration=2100,
            patch=734,
            players=[]
        )

class MockMLflowTracker:
    def log_match_metrics(self, match_data: MatchData) -> None:
        pass

app.dependency_overrides[get_opendota_client] = lambda: MockOpenDotaClient()
app.dependency_overrides[get_mlflow_tracker] = lambda: MockMLflowTracker()

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client