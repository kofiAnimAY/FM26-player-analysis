from app.db.constants import PLAYERS_COLLECTION
from app.db.utils import serialize_item, serialize_items
from app.db import DB
from bson.objectid import ObjectId
from http import HTTPStatus
from datetime import datetime,timedelta,date,time



def _get_player_collection():
    return DB.get_collection(PLAYERS_COLLECTION)

def add_player(**attributes):
    # player_doc={"name":attributes.get("name")}
    player_doc={}
    player_doc.update(attributes)
    result = _get_player_collection().insert_one(player_doc)
    return str(result.inserted_id)

def get_player(name: str):
    player_doc = _get_player_collection().find_one({"name": name})
    if not player_doc:
        return None

    player_doc["id"] = str(player_doc["_id"])
    del player_doc["_id"]
    return player_doc

