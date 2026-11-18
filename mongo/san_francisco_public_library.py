
from pymongo import MongoClient

RESET_COLOR = "\033[0m"
RED_COLOR = "\033[31m"
YELLOW_COLOR = "\033[33m"
CYAN_COLOR = "\033[36m"
GREEN_COLOR = "\033[32m"

try:

    uri = "mongodb://localhost:27017/"
    client = MongoClient(uri)

    client.admin.command("ping")
    print(f"{GREEN_COLOR}Connected successfully{RESET_COLOR}")

    database = client["san_francisco_public_library"]
    collection = database["patron"]

    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

