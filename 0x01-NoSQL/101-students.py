""" function that returns all students sorted by average score: """


def top_students(mongo_collection):
    """ he average score must be part of each item returns with key = averageScore"""
    return list(mongo_collection.find())
