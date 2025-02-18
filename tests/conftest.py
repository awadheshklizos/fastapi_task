
import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.database import init_db
from pymongo import MongoClient
from app.core.config import settings  # Import your settings for the DB connection

@pytest.fixture(scope="session")
def prod_db():
    # client=MongoClient("mongodb://localhost:27017/")
    # db=client["fastapi_testing"]
    # user_collection=db["users"]
    # trash_collection=db["trash"]
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]  

    # db.users.create_index("email", unique=True)
    yield db  
    client.close()

@pytest.fixture(scope="session")
def client(prod_db):
    def override_init_db():
        yield prod_db
    
    app.dependency_overrides[init_db] = override_init_db
    
    with TestClient(app) as test_client:
        yield test_client 

@pytest.fixture(autouse=True)
def cleanup_db(prod_db):
    for collection_name in prod_db.list_collection_names():
        prod_db[collection_name].delete_many({}) 

    yield 
    for collection_name in prod_db.list_collection_names():
        prod_db[collection_name].delete_many({})

