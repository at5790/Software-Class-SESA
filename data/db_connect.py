"""
All interaction with MongoDB should be through this file!
We may be required to use a new database at any point.

Environment variables:
    CLOUD_MONGO: "1" to use the cloud database, "0" (default) for local.
    MONGO_URI: the full connection string for the cloud database,
        e.g. mongodb+srv://<user>:<password>@<cluster-host>/
        Required when CLOUD_MONGO is "1". Never commit it.
    See .env.example in the repo root.
"""
import os
from functools import wraps

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

MONGO_URI = 'MONGO_URI'

SE_DB = 'seDB'
# Database tests use this separate database, so they never touch real data.
TEST_DB = 'seDB_test'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print('Setting client because it is None.')
        # strip() so values sourced from a CRLF .env (which end in \r)
        # still match instead of silently falling back to local
        if os.environ.get('CLOUD_MONGO', LOCAL).strip() == CLOUD:
            uri = os.environ.get(MONGO_URI, '').strip()
            if not uri:
                raise ValueError(f'You must set {MONGO_URI} '
                                 + 'to use Mongo in the cloud.')
            print('Connecting to Mongo in the cloud.')
            client = pm.MongoClient(uri)
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()
    return client


def require_db(fn):
    """
    Ensure a MongoDB connection exists before the decorated function runs.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        connect_db()
        return fn(*args, **kwargs)
    return wrapper


@require_db
def get_collection(collection, db=SE_DB):
    """
    Return a collection, for callers that need to use it directly.
    """
    return client[db][collection]


def convert_mongo_id(doc: dict):
    if MONGO_ID in doc:
        # Convert mongo ID to a string so it works as JSON
        doc[MONGO_ID] = str(doc[MONGO_ID])


@require_db
def create(collection, doc, db=SE_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


@require_db
def create_many(collection, docs, db=SE_DB):
    """
    Insert a list of docs into collection in one call.
    """
    return client[db][collection].insert_many(docs)


@require_db
def read_one(collection, filt, db=SE_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        convert_mongo_id(doc)
        return doc


@require_db
def delete(collection: str, filt: dict, db=SE_DB):
    """
    Find with a filter and return on the first doc found.
    """
    print(f'{filt=}')
    del_result = client[db][collection].delete_one(filt)
    return del_result.deleted_count


@require_db
def drop(collection, db=SE_DB):
    """
    Delete collection and everything in it, including its indexes.
    """
    client[db][collection].drop()


@require_db
def update(collection, filters, update_dict, db=SE_DB):
    return client[db][collection].update_one(filters, {'$set': update_dict})


@require_db
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


@require_db
def fetch_all_as_dict(key, collection, db=SE_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret
