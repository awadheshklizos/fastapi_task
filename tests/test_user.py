# tests/test_users.py
import pytest

def test_create_user(client):
    # Test valid user creation
    response = client.post("/auth/signup/user", json={
        "username":"testdadta",
        "email": "tesdt@example.com",
        "password": "secret"
    })
    assert response.status_code == 201
    data = response.json()


def test_create_admin(client):
    response=client.post("/auth/signup/admin",json={
        "username":"testadmin",
        "email":"testadmin@gmail.com",
        "password":"admin"
    })
    assert response.status_code == 201
    data = response.json()

def test_create_users(client):
    response=client.post("/auth/signup/user",json={
        "username":"testdata2",
        "password":"test@123456789"
    })                                       #missing one field value email,  mismatch schema test
    assert response.status_code ==422







# def test_refresh_token(client):
#     response= client.post("/auth/refresh",json={
#         "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzQwNDA2NDU5fQ.chTCOitx-dm5j_TUO8Xdg5-0HNfaGxkMipHxkv5vpw4"
#         })
#     assert response.status_code == 200 
  


# def test_get_all_users(client):
#     response=client.get("/auth/users")
#     assert response.status_code == 200
