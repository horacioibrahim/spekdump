# -*- coding=UTF-8 -*-

import pymongo

DATABASE = 'serpro'
COLLECTION = 'spekx'


def _get_database(default='mongodb'):
    """ Checks if mongodb is configured perfectly. It's required
    that it exists at least one index in field to not repeat lines
    when to occur new upload (re-run). The defaut database is a 
    collection in MongoDB (serpro.spekx)
    """
    db = DATABASE
    collection = COLLECTION

    try:
        conn =  pymongo.MongoClient()
        database = conn[db]
        col_spekx = database[collection]
    except pymongo.errors.ConnectionFailure, e:
        raise TypeError("Database not is running or it's not using default port")
    
    return col_spekx


if __name__ == "__main__":
    get_database()

