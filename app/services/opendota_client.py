import httpx
import logging
from typing import Optional
from app.core.config import settings
from app.core.exceptions import RateLimitExceeded, OpenDotaAPIError
from app.models.schemas import MatchData

logger = logging.getLogger(__name__)

class OpenDotaClient:
    def __init__(self):
        self.base_url = settings.OPENDOTA_API_BASE_URL
        self.params = {}
        if settings.OPENDOTA_API_KEY:
            self.params["api_key"] = settings.OPENDOTA_API_KEY

    async def fetch_match(self, match_id: int) -> MatchData:
        url = f"{self.base_url}/matches/{match_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=self.params, timeout=10.0)
                
                if response.status_code == 429:
                    logger.warning(f"Rate limit hit for match_id: {match_id}")
                    raise RateLimitExceeded()
                
                response.raise_for_status()
                data = response.json()
                
                if "match_id" not in data:
                    raise OpenDotaAPIError(detail="Malformed match data received from upstream.", status_code=502)
                
                return MatchData(**data)
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code} fetching match {match_id}")
                raise OpenDotaAPIError(detail=f"Upstream API issue: {str(e)}", status_code=e.response.status_code)
            except httpx.RequestError as e:
                logger.error(f"Network error fetching match {match_id}: {str(e)}")
                raise OpenDotaAPIError(detail="Network error reaching OpenDota API.", status_code=503)