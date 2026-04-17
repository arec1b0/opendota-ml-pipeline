from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any

class PlayerMatchData(BaseModel):
    account_id: Optional[int] = Field(default=None, description="Player account ID. Can be None for anonymous players.")
    player_slot: int = Field(default=0, description="Dota 2 engine slot. 0-127 is Radiant, 128-255 is Dire.")
    hero_id: int = Field(default=0, description="Hero ID played.")
    kills: int = Field(default=0)
    deaths: int = Field(default=0)
    assists: int = Field(default=0)
    gold_per_min: Optional[int] = Field(default=None, description="GPM - critical metric, subject to patch drift.")
    xp_per_min: Optional[int] = Field(default=None, description="XPM - critical metric, subject to patch drift.")
    is_radiant: bool = Field(default=False, description="Computed field based on player_slot.")

    @model_validator(mode='before')
    @classmethod
    def compute_is_radiant(cls, data: Any) -> Any:
        if isinstance(data, dict):
            slot = data.get('player_slot', 0)
            data['is_radiant'] = slot < 128
        return data

class MatchData(BaseModel):
    match_id: int = Field(..., description="Unique OpenDota match ID.")
    radiant_win: Optional[bool] = Field(default=None, description="True if Radiant won the match.")
    duration: Optional[int] = Field(default=None, description="Match duration in seconds.")
    patch: Optional[int] = Field(default=None, description="Game patch ID. Used for model degradation monitoring.")
    players: List[PlayerMatchData] = Field(default_factory=list, description="List of player performance data.")