from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos
class Pokemon(BaseModel):
    id: int
    name: str
    type: str
    level: int

# Base de datos simulada
pokemon_db = [
    Pokemon(id=1, name="Pikachu", type="Electric", level=35),
    Pokemon(id=2, name="Charmander", type="Fire", level=12),
    Pokemon(id=3, name="Bulbasaur", type="Grass/Poison", level=15),
]

# Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Pokémon API!"}

@app.get("/pokemon", response_model=List[Pokemon])
def get_all_pokemon():
    return pokemon_db

@app.get("/pokemon/{pokemon_id}", response_model=Pokemon)
def get_pokemon_by_id(pokemon_id: int):
    for pokemon in pokemon_db:
        if pokemon.id == pokemon_id:
            return pokemon
    raise HTTPException(status_code=404, detail="Pokémon not found")

@app.post("/pokemon", response_model=Pokemon)
def add_pokemon(pokemon: Pokemon):
    if any(p.id == pokemon.id for p in pokemon_db):
        raise HTTPException(status_code=400, detail="Pokémon with this ID already exists")
    pokemon_db.append(pokemon)
    return pokemon

@app.delete("/pokemon/{pokemon_id}")
def delete_pokemon(pokemon_id: int):
    for pokemon in pokemon_db:
        if pokemon.id == pokemon_id:
            pokemon_db.remove(pokemon)
            return {"message": "Pokémon deleted successfully"}
    raise HTTPException(status_code=404, detail="Pokémon not found")