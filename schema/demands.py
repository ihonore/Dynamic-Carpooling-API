def individual_serial(demand)->dict:
    return {
        "id":str(demand["_id"]),
        "user_id":str(demand["user_id"]),
        "origin":demand["origin"],
        "destination":demand["destination"],
        "passengers_number":demand["passengers_number"],
        "leaving_at_least":demand["leaving_at_least"],
        "leaving_at_last":demand["leaving_at_last"],
        "arrival_at_least":demand["arrival_at_least"],
        "arrival_at_last":demand["arrival_at_last"],
        "vias":demand["vias"],
        "message":demand["message"],
        "status":demand["status"],
        "created_at":demand["created_at"],
    }

def list_serial(demands)->list:
    return [individual_serial(demand) for demand in demands]