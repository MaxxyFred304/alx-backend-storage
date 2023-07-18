#!/usr/bin/env python3
""" function that lists all documents in a collection """


def list_all(mongo_collection):
    """ function that lists all documents in a collection
        Return an empty list if no document in the collection
    """
    return [each for each in mongo_collection.find()]
