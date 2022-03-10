from threading import local

from pymongo import MongoClient

import settings

_mongo_client = local()


def mongo_client():
    client = getattr(_mongo_client, 'client', None)
    if client is None:
        database_user = settings.DATABASE_USER
        database_password = settings.DATABASE_PASSWORD
        mongo_url = 'mongodb://<' + database_user + '>:<' + database_password + '>@hu-evaluator.cluster-c23hdeqouujb.ap-south-1.docdb.amazonaws.com:27017/?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
        client = MongoClient(mongo_url)
        _mongo_client.client = client
    return client
