from fastapi import FastAPI, HTTPException, status, Request
from dnd_character_sheet.schematic import Character, Identity
from fastapi.responses import JSONResponse
from dnd_character_sheet.db import (
    DatabaseUnavailable,
    CharacterAlreadyExists,
    create_character,
    edit_character,
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


@app.exception_handler(CharacterAlreadyExists)
def handle_character_already_exists(request: Request, exc: CharacterAlreadyExists):
    """Handles the CharacterAlreadyExists exception and returns a 409 Conflict  response."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
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


@app.put("/characters/{name}", response_model=Character)
def edit_existing_character(name: str, updated_character: Character):
    """
    Updates an existing character's information in the MongoDB server.
    
    param:: name: The name of the character to update.
    param:: updated_character: The updated Character object.
    return:: The updated Character.
    """
    result = edit_character(name, updated_character)
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Character not found: {name}")
    return updated_character


@app.post("/characters", response_model=Character, status_code=status.HTTP_201_CREATED)
def create_new_character(character: Character):
    """
    Creates a new character in the MongoDB server.
    
    param:: character: The Character object to create.
    return:: The created Character.
    """
    create_character(character)
    return character