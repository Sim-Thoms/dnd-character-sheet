from typing import Any, ParamSpec, TypeVar
from functools import wraps
from collections.abc import Callable
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
from pymongo.results import InsertOneResult, UpdateResult
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


class CharacterAlreadyExists(Exception):
    """ Custom exception to indicate that a character with the same name already exists in the database."""


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
def create_character(character: Character) -> InsertOneResult:
    """
    Creates a new character in the MongoDB server.
    param:: character: The Character object to create.
    return:: The result of the insert operation.
    raises:: CharacterAlreadyExists if a character with the same name already exists.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]

        if collection.find_one({"identity.name": character.identity.name}):
            raise CharacterAlreadyExists(f"Character with name '{character.identity.name}' already exists.")
        
        return collection.insert_one(character.model_dump(mode="json", by_alias=True))     


@translates_connection_errors
def edit_character(existing_name: str, character: Character) -> UpdateResult:
    """
    Edits an existing character in the MongoDB server.
    param:: existing_name: The name of the character to edit.
    param:: character: The updated Character object.
    return:: The result of the update operation.
    raises:: CharacterAlreadyExists if a character with the new name already exists.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]

        if existing_name != character.identity.name and collection.find_one({"identity.name": character.identity.name}):
            raise CharacterAlreadyExists(f"Character with name '{character.identity.name}' already exists.")
        
        query_filter = {"identity.name": existing_name}
        return collection.replace_one(query_filter, character.model_dump(mode="json", by_alias=True))


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
    character = Character(**character_sheet)

    # List all characters in the database
    characters = list_characters()
    print("Characters in the database:")
    for char in characters:
        print(f"- {char.name} - Lv{char.level} {char.race} {char.class_} ({char.subclass})")

    # Retrieve the character sheet from MongoDB
    from_mongo = get_character(character_sheet['identity']['name'])
    print(from_mongo == character)  # Should print True if the retrieved character matches the original



