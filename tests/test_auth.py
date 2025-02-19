import pytest


def test_login_user(client):
    signup_response=client.post(
        "/auth/signup/admin",json={
            "username":"testing",
            "email":"testing@gmail.com",
            "password":"testing"
        }
    )
    
    assert signup_response.status_code == 201
    user_id=signup_response.json()["id"]
    response=client.post(
        "/auth/login",data={
            "username":"testing",
            "password":"testing"
        }
    )

    assert response.status_code==200
    response_data = response.json()
    
    assert "access_token" in response_data
    assert "refresh_token" in response_data


    #test case for regenerate access Token using refresh Token
def test_regenerate_refresh_token(client):
    response=client.post("/auth/signup/user",json={
        "username":"testadmin",
        "email":"testadmin@gmail.com",
        "password":"testadmin"    
    })

    assert response.status_code == 201
    assert response.json()['username']  == "testadmin"
    
    login_res=client.post("/auth/login",data={
        "username":"testadmin",
        "password":"testadmin"
    })

    assert login_res.status_code == 200
    res_data = login_res.json()

    refresh_token=res_data['refresh_token']
    refresh_token_res=client.post(f"/auth/refresh/{refresh_token}",json={
        "refresh_token":refresh_token
    })
    assert refresh_token_res.status_code == 200
    # print(refresh_token_res.json())

