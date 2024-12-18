import data.db_connect as dbc

TEXT_COLLECTION = 'texts'

KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'


def convert_mongo_id(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


def read():
    texts = dbc.read(TEXT_COLLECTION)
    return [convert_mongo_id(text) for text in texts]


def create(key, title, text, email):
    if dbc.get_one(TEXT_COLLECTION, {KEY: key}):
        raise ValueError(f"Entry with key '{key}' already exists.")
    new_entry = {
        KEY: key,
        TITLE: title,
        TEXT: text,
        EMAIL: email,
    }
    result = dbc.create(TEXT_COLLECTION, new_entry)
    new_entry["_id"] = str(result.inserted_id)
    return new_entry


def get_one(key: str):
    text = dbc.get_one(TEXT_COLLECTION, {KEY: key})
    return convert_mongo_id(text) if text else {}


def update(key, title=None, text=None, email=None):
    entry = dbc.get_one(TEXT_COLLECTION, {KEY: key})
    if not entry:
        raise ValueError(f"Entry with key '{key}' does not exist.")
    updates = {}
    if title:
        updates[TITLE] = title
    if text:
        updates[TEXT] = text
    if email:
        updates[EMAIL] = email
    dbc.update_doc(TEXT_COLLECTION, {KEY: key}, updates)
    updated_entry = dbc.get_one(TEXT_COLLECTION, {KEY: key})
    return convert_mongo_id(updated_entry) if updated_entry else {}


def delete(key):
    result = dbc.del_one(TEXT_COLLECTION, {KEY: key})
    if result == 0:
        raise ValueError(f"Entry with key '{key}' does not exist.")
    return key
