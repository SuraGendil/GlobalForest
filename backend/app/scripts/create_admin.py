import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.user_controller import create_user
from app.models.user import User

# Create admin user
admin_user = User(username="admin", password="admin", email="admin@example.com", role="admin")
try:
    user_id = create_user(admin_user)
    print(f"Admin user created with ID: {user_id}")
except Exception as e:
    print(f"Error: {e}")