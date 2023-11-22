def individual_serial(demand)->dict:
    return {
        "id":str(demand["_id"]),
        "user_id":str(demand["user_id"]),
        "origin":demand["origin"],
        "destination":demand["destination"],
        "departure_time":demand["departure_time"],
        "arrival_time":demand["arrival_time"],
        "message":demand["message"],
        "status":demand["status"],
        "created_at":demand["created_at"],
    }

def list_serial(demands)->list:
    return [individual_serial(demand) for demand in demands]