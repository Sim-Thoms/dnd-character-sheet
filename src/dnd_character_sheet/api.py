from fastapi import FastAPI, HTTPException, status, Request
from dnd_character_sheet.schematic import Character, Identity
from fastapi.responses import JSONResponse
from dnd_character_sheet.db import (
    DatabaseUnavailable,
    list_characters,
    get_character,
)

app = FastAPI()


@app.exception_handler(DatabaseUnavailable)
def handle_database_unavailable(request: Request, exc: DatabaseUnavailable):
    """Handles the DatabaseUnavailable exception and returns a 503 Service Unavailable response."""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "MongoDB is currently unavailable. Please try again later."},
    )


@app.get("/characters", response_model=list[Identity])
def get_characters():
    """ Returns a list of all characters' identities in the MongoDB server."""
    return list_characters()


@app.get("/characters/{name}", response_model=Character)
def get_character_by_name(name: str):
    """
    Returns a character's information from the MongoDB server by name.
    
    param:: name: The name of the character to retrieve.
    return:: The validated Character.
    """
    # Why did I include this? Because I can. And because it's funny.
    if name.lower() == "coffee":
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)

    character = get_character(name)
    if character is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character not found: {name}")

    return character

