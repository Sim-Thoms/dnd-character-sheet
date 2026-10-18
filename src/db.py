from pymongo.server_api import ServerApi
from pymongo import MongoClient
from dotenv import load_dotenv
import os 



def get_mongo_client():
    """
    Returns a MongoClient instance connected to the MongoDB server.
    """
    load_dotenv()

    # Create a new client and connect to the server
    return MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))

def get_character_doc(db_name: str, collection_name: str, document_name: str) -> dict:
    """
    Returns a character's information from the MongoDB server.

    param:: db_name: The name of the database.
    param:: collection_name: The name of the collection.
    param:: document_name: The name of the document to fetch.
    return:: The document as a dictionary.
    """
    client = get_mongo_client()
    return client[db_name][collection_name].find_one({"identity.name": document_name})



if __name__ == "__main__":
    ## 0 - Temporary upload of a character sheet to the database for testing purposes
    import yaml

    YAML_FILE = "Mossy Endoxy.yaml"
    with open(f"data/raw/{YAML_FILE}", "r", encoding="utf-8") as f:
        character_sheet = yaml.safe_load(f)

    with get_mongo_client() as client:
        db = client["DnD"]
        collection = db["character_sheets"]

        # Insert the data into MongoDB
        query_filter = {"identity.name": character_sheet["identity"]["name"]}
        result = collection.replace_one(query_filter, character_sheet, upsert=True)

        if result.upserted_id:
            print(f"{character_sheet["identity"]["name"]} was successfully uploaded to MongoDB")
        else: 
            print(f"{character_sheet["identity"]["name"]} was successfully updated on MongoDB")
    
    ## 1 - Fetch character sheet from MongoDB
    character_name = "Mossy Endoxy"
    character_doc = get_character_doc("DnD", "character_sheets", character_name)
    print(character_doc)





