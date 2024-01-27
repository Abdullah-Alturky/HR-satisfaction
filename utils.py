def stringify_mongo_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj


def paginate(records, page, limit):
    return records.skip((page - 1) * limit).limit(limit)
