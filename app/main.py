from fastapi import FastAPI, HTTPException
from typing import List, Optional

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="Pokémon API",
    description="Una API para explorar información sobre Pokémon.",
    version="1.0.0"
)

# Datos de ejemplo
pokemon_data = [
    {
        "id": 1,
        "name": "Bulbasaur",
        "type": ["Grass", "Poison"],
        "abilities": ["Overgrow", "Chlorophyll"],
        "base_stats": {"hp": 45, "attack": 49, "defense": 49, "speed": 45},
        "evolution": {"next": "Ivysaur", "level": 16}
    },
    {
        "id": 4,
        "name": "Charmander",
        "type": ["Fire"],
        "abilities": ["Blaze", "Solar Power"],
        "base_stats": {"hp": 39, "attack": 52, "defense": 43, "speed": 65},
        "evolution": {"next": "Charmeleon", "level": 16}
    },
    {
        "id": 7,
        "name": "Squirtle",
        "type": ["Water"],
        "abilities": ["Torrent", "Rain Dish"],
        "base_stats": {"hp": 44, "attack": 48, "defense": 65, "speed": 43},
        "evolution": {"next": "Wartortle", "level": 16}
    },
    {
        "id": 25,
        "name": "Pikachu",
        "type": ["Electric"],
        "abilities": ["Static", "Lightning Rod"],
        "base_stats": {"hp": 35, "attack": 55, "defense": 40, "speed": 90},
        "evolution": {"next": "Raichu", "level": "Use Thunder Stone"}
    }
]

# Endpoints de la API
@app.get("/pokemon", response_model=List[dict])
def get_all_pokemon(skip: int = 0, limit: int = 10):
    """
    Obtén una lista de Pokémon con soporte para paginación.
    """
    return pokemon_data[skip:skip + limit]

@app.get("/pokemon/{name}", response_model=dict)
def get_pokemon_by_name(name: str):
    """
    Obtén los detalles de un Pokémon por su nombre.
    """
    for pokemon in pokemon_data:
        if pokemon["name"].lower() == name.lower():
            return pokemon
    raise HTTPException(status_code=404, detail="Pokémon not found")

@app.get("/pokemon/type/{type_name}", response_model=List[dict])
def get_pokemon_by_type(type_name: str):
    """
    Filtra los Pokémon por su tipo.
    """
    filtered_pokemon = [p for p in pokemon_data if type_name.capitalize() in p["type"]]
    if not filtered_pokemon:
        raise HTTPException(status_code=404, detail="No Pokémon found for this type")
    return filtered_pokemon

@app.get("/pokemon/average-stats", response_model=dict)
def get_average_stats():
    """
    Calcula los promedios de estadísticas base de todos los Pokémon.
    """
    total_stats = {"hp": 0, "attack": 0, "defense": 0, "speed": 0}
    for pokemon in pokemon_data:
        for stat, value in pokemon["base_stats"].items():
            total_stats[stat] += value
    count = len(pokemon_data)
    return {stat: round(value / count, 2) for stat, value in total_stats.items()}

@app.get("/pokemon/search", response_model=List[dict])
def search_pokemon(
    type: Optional[str] = None,
    ability: Optional[str] = None
):
    """
    Filtra Pokémon por tipo y/o habilidad.
    """
    filtered_pokemon = pokemon_data
    if type:
        filtered_pokemon = [p for p in filtered_pokemon if type.capitalize() in p["type"]]
    if ability:
        filtered_pokemon = [p for p in filtered_pokemon if ability.capitalize() in p["abilities"]]
    if not filtered_pokemon:
        raise HTTPException(status_code=404, detail="No Pokémon match the search criteria")
    return filtered_pokemon