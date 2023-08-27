def get_user_by_id(id, data):
    for user in data:
        if user["id"] == id:
            return user
    return None