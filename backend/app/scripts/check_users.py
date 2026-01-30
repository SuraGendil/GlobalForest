import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.user_controller import get_users

users = get_users()
print("Users in DB:", users)