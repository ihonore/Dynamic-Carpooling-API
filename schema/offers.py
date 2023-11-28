def individual_serial(offer) -> dict:
    try:
        return {
            "id": str(offer["_id"]),
            "user_id": str(offer["user_id"]),
            "itinerary": offer["itinerary"],
            "plate_number": offer["plate_number"],
            "available_seats": offer["available_seats"],
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
