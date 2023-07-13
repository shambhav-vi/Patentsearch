from pyArango.connection import *
from django.conf import settings

def connect_to_arangodb():
    conn = Connection(
            arangoURL=f"http://{settings.ARANGO_HOST}:{settings.ARANGO_PORT}",
            username=settings.ARANGO_USERNAME,
            password=settings.ARANGO_PASSWORD
        )
    
    db = conn[settings.ARANGO_DB_NAME]
    
    if not db.hasCollection("user"):
        collection = db.createCollection(name="user")

    return db