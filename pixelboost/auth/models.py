from beanie import PydanticObjectId
import bcrypt
from pixelboost.models import BaseUser


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)

class UserRead(BaseUser):
    id: PydanticObjectId
