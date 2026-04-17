from fastapi import HTTPException, status

class OpenDotaAPIError(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(status_code=status_code, detail=detail)

class RateLimitExceeded(OpenDotaAPIError):
    def __init__(self):
        super().__init__(
            detail="OpenDota API rate limit exceeded. Check API key or scale down requests.", 
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

class DataDriftAnomaly(Exception):
    """Raised when incoming match metrics deviate significantly from expected baselines."""
    pass