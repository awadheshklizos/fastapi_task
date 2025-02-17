# # tests/test_auth.py
# def test_login(client):
#     # Create user first
#     client.post("/users/", json={
#         "email": "login@test.com",
#         "password": "secret"
#     })
    
#     # Test valid login
#     response = client.post("/login", data={
#         "username": "login@test.com",
#         "password": "secret"
#     })
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# def test_invalid_login(client):
#     # Test invalid credentials
#     response = client.post("/login", data={
#         "username": "nonexistent@test.com",
#         "password": "wrong"
#     })
#     assert response.status_code == 401











# # tests/test_auth.py

# from fastapi.testclient import TestClient
# from main import app  # Import the FastAPI app from main.py
# import pytest
# from app.models.user_model import User
# from app.core.security import get_password_hash
# from httpx import AsyncClient

# client = TestClient(app)

# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "FoR Test the code "}


# @pytest.fixture(scope="module")
# async def db_client():
#     # Setup the test database connection
#     client = AsyncIOMotorClient(settings.MONGO_URI)
#     db = client.get_database()
#     await init_db()
#     yield db
#     client.close()

# @pytest.fixture(autouse=True)
# async def setup_and_teardown():
#     await User.delete_all()
#     yield
#     await User.delete_all()

# @pytest.mark.asyncio
# async def test_signup_user(db_client):
#     user_data = {
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "password": "password"
#     }

#     # Use AsyncClient to make an async request
#     async with AsyncClient(base_url="http://test") as clients:
#         response = await clients.post("/auth/signup/user", json=user_data)
        
#     # Check the response
#     assert response.status_code == 201
#     assert "username" in response.json()
#     assert response.json()["username"] == "testuser"



# @pytest.mark.asyncio
# async def test_signup_admin(db_client):
#     admin_data = {
#         "username": "testadmin",
#         "email": "testadmin@example.com",
#         "password": "password"
#     }
#     response = client.post("/auth/signup/admin", json=admin_data)
#     assert response.status_code == 201
#     assert "username" in response.json()
#     assert response.json()["role"] == "admin"

# @pytest.mark.asyncio
# async def test_login(db_client):
#     # Create a user for login
#     user = User(
#         username="testuser",
#         email="testuser@example.com",
#         hashed_password=get_password_hash("password"),
#         role="user"
#     )
#     await user.insert()

#     login_data = {"username": "testuser", "password": "password"}
#     response = client.post("/auth/login", data=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert "refresh_token" in response.json()

# tests/test_auth.py

# from fastapi.testclient import TestClient
# from main import app 
# import json
# import pytest
# from httpx import AsyncClient

# client = TestClient(app)

# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "FoR Test the code "}

# @pytest.mark.asyncio
# async def test_signup_user():
#     user_data = {
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "password": "password"
#     }

#     # Use AsyncClient for async requests in tests
#     async with AsyncClient( base_url="http://test") as client:
#         response = await client.post("/auth/signup/user", json=user_data)

#     # Check the response
#     assert response.status_code == 201
#     assert "username" in response.json()
#     assert response.json()["username"] == "testuser"



    # assert response.json()["username"] == "newuser"
    # assert response.json()["email"] == "newuser@example.com"
    # assert response.json()["role"] == "user"

# def test_signup_admin():
#     admin_data = {
#         "username": "adminuser",
#         "email": "adminuser@example.com",
#         "password": "adminpassword"
#     }
#     response = client.post("/auth/signup/admin", json=admin_data)
#     assert response.status_code == 201
#     assert response.json()["username"] == "adminuser"
#     assert response.json()["role"] == "admin"

# def test_login():
#     login_data = {
#         "username": "adminuser",
#         "password": "adminpassword"
#     }
#     response = client.post("/auth/login", data=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert "refresh_token" in response.json()
