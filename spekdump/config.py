# -*- coding=UTF-8 -*-

import pymongo

DATABASE = 'serpro'
COLLECTION = 'spekx'


def get_database(host=None, database=None, collection=None, default='mongodb'):
    """ Checks if mongodb is configured perfectly. It's required
    that it exists at least one index in field to not repeat lines
    when to occur new upload (re-run). The defaut database is a 
    collection in MongoDB (serpro.spekx)
    """

    if host is None:
        host = '127.0.0.1' # Default host

    if database is None:
        database = DATABASE # database name default

    if collection is None:
        collection = COLLECTION # collection default

    try:
        conn =  pymongo.MongoClient(host=host, port=27017)
        db = conn[database]
        col_spekx = db[collection]
    except pymongo.errors.ConnectionFailure, e:
        raise TypeError("Database not is running or it's not using default port")
    
    return col_spekx


if __name__ == "__main__":
    get_database()

