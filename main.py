from fastapi import FastAPI, Depends
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
import requests
from app.models import Base
from app.models import Character
from app.database import get_db
from app.database import engine
from typing import List

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/scrape_character")
async def scrape_character(url: str, db: Session = Depends(get_db)):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # Extract the character information from the HTML
    name = soup.find('span', class_='long-title').text.strip()
    description = soup.find('p', class_='desc').text.strip()
    appearances = [a.text.strip() for a in soup.select('.category:has(.heading:-soup-contains("Appearances")) a')]
    affiliations = [a.text.strip() for a in soup.select('.category:has(.heading:-soup-contains("Affiliations")) a')]
    locations = [a.text.strip() for a in soup.select('.category:has(.heading:-soup-contains("Locations")) a')]
    dimensions = [d.text.strip() for d in soup.select('.category:has(.heading:-soup-contains("Dimensions")) .property-name')]
    weapons = [w.text.strip() for w in soup.select('.category:has(.heading:-soup-contains("Weapons")) a')]
    vehicles = [v.text.strip() for v in soup.select('.category:has(.heading:-soup-contains("Vehicles")) a')]
    tools = [t.text.strip() for t in soup.select('.category:has(.heading:-soup-contains("Tool")) a')]

    character_data = Character(
        name=name,
        description=description,
        appearances=",".join(appearances),
        affiliations=",".join(affiliations),
        locations=",".join(locations),
        dimensions=",".join(dimensions),
        weapons=",".join(weapons),
        vehicles=",".join(vehicles),
        tools=",".join(tools)
    )
    db.add(character_data)
    db.commit()
    db.refresh(character_data)

    # Return the scraped character data
    character = Character(
        name=name,
        description=description,
        appearances=appearances,
        affiliations=affiliations,
        locations=locations,
        dimensions=dimensions,
        weapons=weapons,
        vehicles=vehicles,
        tools=tools
    )
    return character

@app.post("/manualy_create_character")
async def create_character(
    name: str,
    description: str,
    appearances: List[str] = [],
    affiliations: List[str] = [],
    locations: List[str] = [],
    dimensions: List[str] = [],
    weapons: List[str] = [],
    vehicles: List[str] = [],
    tools: List[str] = [],
    db: Session = Depends(get_db)
):
    character_data = Character(
        name=name,
        description=description,
        appearances=",".join(appearances),
        affiliations=",".join(affiliations),
        locations=",".join(locations),
        dimensions=",".join(dimensions),
        weapons=",".join(weapons),
        vehicles=",".join(vehicles),
        tools=",".join(tools)
    )
    db.add(character_data)
    db.commit()
    db.refresh(character_data)
    return character_data