from pymongo import MongoClient

from src.utils.errors import API_ERROR


class MongoDB:

    def __init__(self, conn_string):
        self.mongo_client = MongoClient(conn_string)
        self.db = self.mongo_client.get_database()

    def find(self, collection_name, where, select=None):
        collection = self.db[collection_name]
        try:
            if not select:
                select = None

            cursor = collection.find(where, select).max_time_ms(5000)

            items = list(cursor)

            return items

        except Exception as e:
            raise API_ERROR(
                message="Cannot perform MongoDB 'find' operation",
                status_code=503,
                details=str(e),
                error_type="databaseError"
            )
