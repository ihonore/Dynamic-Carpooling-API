def individual_serial(demand)->dict:
    return {
        "id":str(demand["_id"]),
        "user_id":str(demand["user_id"]),
        "itinerary": demand["itinerary"],
        #"passengers_number":demand["passengers_number"],
        "message":demand["message"],
        "status":demand["status"],
        "created_at":demand["created_at"],
        
        "plate_number": demand["plate_number"],
        "available_seats": demand["available_seats"],
    }

def list_serial(demands)->list:
    return [individual_serial(demand) for demand in demands]