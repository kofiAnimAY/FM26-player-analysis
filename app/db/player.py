from app.db.constants import PLAYERS_COLLECTION
from app.db.utils import serialize_item, serialize_items
from app.db import DB
from bson.objectid import ObjectId
from http import HTTPStatus
from datetime import datetime,timedelta,date,time



def _get_event_collection():
    return DB.get_collection(PLAYERS_COLLECTION)

def add_player():
    player_doc = {

    }
    result = _get_event_collection().insert_one(player_doc)
    return str(result.inserted_id)