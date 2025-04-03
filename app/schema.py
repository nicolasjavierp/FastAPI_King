from pydantic import BaseModel
from typing import List

class Character(BaseModel):
    name: str
    description: str
    species: str
    homeworld: str
    appearances: List[str] = []
    affiliations: List[str] = []
    locations: List[str] = []
    dimensions: List[str] = []
    weapons: List[str] = []
    vehicles: List[str] = []
    tools: List[str] = []
