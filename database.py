# database.py

# In a real application, this would be a connection to a database like PostgreSQL, MySQL, etc.
# For this example, we use a simple in-memory dictionary.
# Key: email (str), Value: dict of user data (e.g., {"email": "...", "hashed_password": "...", "is_active": True})
users_db = {}

def get_user(email: str):
    """Retrieve a user by email."""
    return users_db.get(email)

def create_user(user_data: dict):
    """Add a new user to the database."""
    email = user_data["email"]
    if email in users_db:
        return None  # User already exists
    users_db[email] = user_data
    return users_db[email]

def update_user(email: str, update_data: dict):
    """Update user data."""
    if email in users_db:
        users_db[email].update(update_data)
        return users_db[email]
    return None
