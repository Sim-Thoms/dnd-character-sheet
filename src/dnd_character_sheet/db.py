from typing import Any, ParamSpec, TypeVar
from functools import wraps
from collections.abc import Callable
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from dnd_character_sheet.schematic import (
    Character,
    Identity,
)

DATABASE = "DnD"
COLLECTION = "character_sheets"
P = ParamSpec("P")
R = TypeVar("R")


class DatabaseUnavailable(Exception):
    """ Custom exception to indicate that the MongoDB server is unavailable."""


def translates_connection_errors(func: Callable[P, R]) -> Callable[P, R]:
    """
    A decorator that translates pymongo ConnectionFailure exceptions into a custom DatabaseUnavailable exception.
    
    param:: func: The function to decorate.
    return:: The decorated function that raises DatabaseUnavailable on ConnectionFailure.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except ConnectionFailure as err:
            raise DatabaseUnavailable(str(err)) from err
    return wrapper


def open_mongo_client()-> MongoClient[dict[str, Any]]:
    """
    Returns a MongoClient instance connected to the MongoDB server.
    """
    load_dotenv()

    # Create a new client and connect to the server
    return MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))


@translates_connection_errors
def save_character(character: Character):
    """
    Saves a character's information to the MongoDB server.

    param:: character: The Character object to save.
    return:: The result of the upsert operation.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        query_filter = {"identity.name": character.identity.name}
        result = collection.replace_one(query_filter, character.model_dump(mode="json", by_alias=True), upsert=True)
        return result      


@translates_connection_errors
def get_character(character_name: str) -> Character | None:
    """
    Returns a character's information from the MongoDB server.

    param:: character_name: The name of the character to retrieve.
    return:: The validated Character or None if not found.
    """

    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        doc = collection.find_one({"identity.name": character_name}) # Returns None if no document is found with the specified name
        return Character(**doc) if doc else None


@translates_connection_errors
def list_characters() -> list[Identity]:
    """
    Returns a list of all character names in the MongoDB server.

    return:: A list of characters' identities.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        cursor = collection.find({}, {"identity": 1, "_id": 0}).sort("identity.name")
        return [Identity(**doc["identity"]) for doc in cursor]


if __name__ == "__main__":
    import yaml

    YAML_FILE = "Mossy Endoxy.yaml"
    with open(f"data/raw/{YAML_FILE}", "r", encoding="utf-8") as f:
        character_sheet = yaml.safe_load(f)

    # Save the character sheet to MongoDB
    character = Character(**character_sheet)
    result = save_character(character)
    if result.upserted_id:
        print(f"{character_sheet['identity']['name']} was successfully uploaded with ID: {result.upserted_id}")
    else: 
        print(f"{character_sheet['identity']['name']} was successfully updated. Matched: {result.matched_count}")

    # List all characters in the database
    characters = list_characters()
    print("Characters in the database:")
    for char in characters:
        print(f"- {char.name} - Lv{char.level} {char.race} {char.class_} ({char.subclass})")

    # Retrieve the character sheet from MongoDB
    from_mongo = get_character(character_sheet['identity']['name'])
    print(from_mongo == character)  # Should print True if the retrieved character matches the original



