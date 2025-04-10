from starlette.config import Config
import os

config = Config(".env")

def get_config(key):
    return os.getenv(key) or config(key)


# DATABASE
DATABASE_CREDENTIALS = get_config("DATABASE_CREDENTIALS")
_DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")
DATABASE_CLUSTER_NAME = get_config("DATABASE_CLUSTER_NAME")
DATABASE_CLUSTER_ID = get_config("DATABASE_CLUSTER_ID")
DATABASE_NAME = get_config("DATABASE_NAME")
MONGO_DATABASE_URI = f"mongodb+srv://{_DATABASE_CREDENTIAL_USER}:{_DATABASE_CREDENTIAL_PASSWORD}@{DATABASE_CLUSTER_NAME}.{DATABASE_CLUSTER_ID}.mongodb.net/?retryWrites=true&w=majority&appName={DATABASE_CLUSTER_NAME}"

# JWT
JWT_SECRET = get_config("JWT_SECRET")
JWT_ALG = get_config("JWT_ALG")
JWT_EXP = get_config("JWT_EXP")
JWT_REFRESH_SECRET = get_config("JWT_REFRESH_SECRET")
JWT_REFRESH_ALG = get_config("JWT_REFRESH_ALG")
JWT_REFRESH_EXP = get_config("JWT_REFRESH_EXP")
