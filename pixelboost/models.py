from beanie import Document
from pydantic import EmailStr


# MongoDB
class User(Document):
    username: str
    email: EmailStr
    is_verified: bool = False
    password: str

    name: str

    class Settings:
        name = "users"
