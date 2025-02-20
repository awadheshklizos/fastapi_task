
import sys
import os
import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db
from pymongo import MongoClient
from app.core.config import settings 
import asyncio


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope='session')
def prod_db():

    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]  
    yield db  
    client.close()

@pytest.fixture(scope='session')
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

