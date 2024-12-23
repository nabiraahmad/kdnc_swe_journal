import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

SE_DB = 'JournalDB'

client = None

MONGO_ID = '_id'
database = None


def connect_db():
    global client
    if client is None:
        try:
            if os.environ.get('CLOUD_MONGO', LOCAL) == CLOUD:
                password = os.environ.get("GAME_MONGO_PW")
                if not password:
                    raise ValueError(
                        'You must set your password to use Mongo in the cloud.'
                    )
                print('Connecting to Mongo in the cloud.')
                mongo_uri = (
                    f'mongodb+srv://ktn3138:{password}'
                    '@kdnc.g7lnd.mongodb.net/'
                    '?retryWrites=true&w=majority&appName=KDNC'
                )
                client = pm.MongoClient(mongo_uri)
            else:
                print('Connecting to Mongo locally.')
                client = pm.MongoClient()

            # Test the connection
            client.server_info()
            print("MongoDB connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise e
    return client


def convert_mongo_id(doc: dict):
    if MONGO_ID in doc:
        doc[MONGO_ID] = str(doc[MONGO_ID])


def create(collection, doc, db=SE_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def get_one(collection, filt, db=SE_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        convert_mongo_id(doc)
        return doc


def del_one(collection, filt, db=SE_DB):
    """
    Find with a filter and return on the first doc found.
    """
    del_result = client[db][collection].delete_one(filt)
    return del_result.deleted_count


def update_doc(collection, filters, update_dict, db=SE_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


def fetch_one(db_mn, clct_nm, filters={}, no_id=False):
    return get_one(db_mn, clct_nm, filters=filters, no_id=no_id)


def read(collection, db=SE_DB, no_id=True) -> list:
    """
    Returns a list from the db.
    """
    ret = []
    for doc in client[db][collection].find():
        if no_id:
            del doc[MONGO_ID]
        else:
            convert_mongo_id(doc)
        ret.append(doc)
    return ret


def read_dict(collection, key, db=SE_DB, no_id=True) -> dict:
    recs = read(collection, db=db, no_id=no_id)
    recs_as_dict = {}
    for rec in recs:
        recs_as_dict[rec[key]] = rec
    return recs_as_dict


def fetch_all_as_dict(key, collection, db=SE_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


# @needs_db
def fetch_by_id(db_num, clct_nm, _id: str, no_id=False):
    return database.fetch_by_id(db_num, clct_nm, _id, no_id=no_id)
