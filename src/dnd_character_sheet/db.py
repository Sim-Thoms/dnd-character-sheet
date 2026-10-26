from typing import Any, ParamSpec, TypeVar
from functools import wraps
from collections.abc import Callable
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from dnd_character_sheet.schema import (
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


class CharacterNotFound(Exception):
    """ Custom exception to indicate that a character was not found in the database."""


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
    raises:: CharacterNotFound if the character to edit does not exist.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]    

        if existing_name != character.identity.name and collection.find_one({"identity.name": character.identity.name}):
            raise CharacterAlreadyExists(f"Character with name '{character.identity.name}' already exists.")

        query_filter = {"identity.name": existing_name}
        result = collection.replace_one(query_filter, character.model_dump(mode="json", by_alias=True))

        if result.matched_count == 0:
            raise CharacterNotFound(f"Character with name '{existing_name}' not found.")    
        
        return result


@translates_connection_errors
def get_character(character_name: str) -> Character:
    """
    Returns a character's information from the MongoDB server.

    param:: character_name: The name of the character to retrieve.
    return:: The validated Character.
    raises:: CharacterNotFound if the character does not exist.
    """

    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        result = collection.find_one({"identity.name": character_name}) # Returns None if no document is found with the specified name

        if result is None:
            raise CharacterNotFound(f"Character with name '{character_name}' not found.")

        return Character(**result)


@translates_connection_errors
def list_characters() -> list[Identity]:
    """
    Returns a list of all characters' identities.

    return:: A list of characters' identities.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        cursor = collection.find({}, {"identity": 1, "_id": 0}).sort("identity.name")
        return [Identity(**doc["identity"]) for doc in cursor]


@translates_connection_errors
def delete_character(character_name: str) -> DeleteResult:
    """
    Deletes a character from the MongoDB server.

    param:: character_name: The name of the character to delete.
    return:: The result of the delete operation.
    raises:: CharacterNotFound if the character does not exist.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        result = collection.delete_one({"identity.name": character_name})

        if result.deleted_count == 0:
            raise CharacterNotFound(f"Character with name '{character_name}' not found.")
        
        return result



