def individual_serial(user)->dict:
    return {
        "id":str(user["_id"]),
        "username":user["username"],
        "email":user["email"],
        "full_name":user["full_name"],
        "phone_number":user["phone_number"],
        "role":user["role"],
        "created_at":user["created_at"],
    }

def list_serial(users)->list:
    return [individual_serial(user) for user in users]