from beanie import Document

# MongoDB
class User(Document):
    username: str
    password: str

    class Settings:
        name = "users"
