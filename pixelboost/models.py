from beanie import Document

class BaseUser(Document):
    username: str
    password: str

    class Settings:
        name = "users"
