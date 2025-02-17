# tests/conftest.py
# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from app.core.database import init_db
# import mongomock



# @pytest.fixture(scope="module")
# def test_db():
#     # Use mongomock for testing
#     client = mongomock.MongoClient()
#     db = client.get_database("test_db")
#     yield db
#     client.drop_database("test_db")

# @pytest.fixture(scope="module")
# def client(test_db):
#     # Override database dependency
#     def override_test_db():
#         yield test_db
    
#     app.dependency_overrides[test_db] = override_test_db
#     with TestClient(app) as client:
#         yield client


 
# @pytest.fixture(autouse=True)
# async def setup_and_teardown():
#     await User.delete_all()
#     yield
#     await User.delete_all()



import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.database import init_db
from pymongo import MongoClient
from app.core.config import settings  # Import your settings for the DB connection

@pytest.fixture(scope="session")
def prod_db():
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]  

    db.users.create_index("email", unique=True)
    
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
