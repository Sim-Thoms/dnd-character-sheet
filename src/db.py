from pydoc import doc
from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv
import os 
from schematic import (
    Character,
    Identity,
)

DATABASE = "DnD"
COLLECTION = "character_sheets"


def open_mongo_client():
    """
    Returns a MongoClient instance connected to the MongoDB server.
    """
    load_dotenv()

    # Create a new client and connect to the server
    return MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))


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


def get_character(character_name: str) -> Character:
    """
    Returns a character's information from the MongoDB server.

    param:: character_name: The name of the character to retrieve.
    return:: The validated Character.
    raise:: ValueError if no character with that name exists.
    """
    with open_mongo_client() as client:
        db = client[DATABASE]
        collection = db[COLLECTION]
        doc = collection.find_one({"identity.name": character_name})
        if doc is None:
            raise ValueError(f"Character not found: {character_name}")
        return Character(**doc)


def list_characters() -> list[Identity]:
    """
    Returns a list of all character names in the MongoDB server.

    return:: A list of character names.
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



