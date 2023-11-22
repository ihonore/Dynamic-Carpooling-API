def individual_serial(offer)->dict:
    return {
        "id":str(offer["_id"]),
        "user_id":str(offer["user_id"]),
        "origin":offer["origin"],
        "destination":offer["destination"],
        "plate_number":offer["plate_number"],
        "available_seats":offer["available_seats"],
        "departure_time":offer["departure_time"],
        "arrival_time":offer["arrival_time"],
        "message":offer["message"],
        "created_at":offer["created_at"],
    }

def list_serial(offers)->list:
    return [individual_serial(offer) for offer in offers]