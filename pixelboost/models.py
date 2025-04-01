from beanie import Document
from pydantic import EmailStr, Field

# MongoDB
class User(Document):
    username: str
    email: EmailStr
    is_verified: bool = False
    password: str

    class Settings:
        name = "users"
