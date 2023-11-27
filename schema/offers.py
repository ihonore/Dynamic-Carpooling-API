def individual_serial(offer)->dict:
    return {
        "id":str(offer["_id"]),
        "user_id":str(offer["user_id"]),
        "origin":offer["origin"],
        "destination":offer["destination"],
        "plate_number":offer["plate_number"],
        "available_seats":offer["available_seats"],
        "leaving_at_least":offer["leaving_at_least"],
        "leaving_at_last":offer["leaving_at_last"],
        "arrival_at_least":offer["arrival_at_least"],
        "arrival_at_last":offer["arrival_at_last"],
        "via":offer["via"],
        "message":offer["message"],
        "created_at":offer["created_at"],
    }

def list_serial(offers)->list:
    return [individual_serial(offer) for offer in offers]