def individual_serial(offer) -> dict:
    try:
        return {
            "id": str(offer["_id"]),
            "user_id": str(offer["user_id"]),
            "origin": offer["origin"],
            "destination": offer["destination"],
            "plate_number": offer["plate_number"],
            "available_seats": offer["available_seats"],
            "leaving_at_least": offer["leaving_at_least"],
            "leaving_at_last": offer["leaving_at_last"],
            "arrival_at_least": offer["arrival_at_least"],
            "arrival_at_last": offer["arrival_at_last"],
            "vias": offer["vias"],
            "message": offer["message"],
            "created_at": offer["created_at"],
        }
    except KeyError as e:
        raise ValueError(f"KeyError in individual_serial: {str(e)}")

def list_serial(offers) -> list:
    try:
        return [individual_serial(offer) for offer in offers]
    except Exception as e:
        raise ValueError(f"Error in list_serial: {str(e)}")
