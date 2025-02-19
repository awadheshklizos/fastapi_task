
import pytest
from bson import ObjectId 


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

def test_create_user2(client):
    response=client.post("/auth/signup/user",json={
        "username":"testdata2",
        "password":"test@123456789"
    })                                
    assert response.status_code == 422      #missing email field mismatch validation


def test_get_all_users(client):
    signup_response=client.post(
        "/auth/signup/admin",json={
            "username":"test1",
            "email":"test1@gmail.com",
            "password":"test1"
        } )
    assert signup_response.status_code == 201

    signup_data= signup_response.json()

    response=client.post(
        "/auth/login",data={
            "username":"test1",
            "password":"test1"
        }
    )

    assert response.status_code==200
    response_data = response.json()
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    res = client.get("/auth/users", headers=headers)  
    assert res.status_code == 200


def test_get_user_by_id(client):
    signup_response=client.post(
        "/auth/signup/admin",json={
            "username":"test2", "email":"test2@gmail.com", "password":"test2" })
    assert signup_response.status_code == 201
    signup_data= signup_response.json()
    user_id = signup_data["id"]
    
    response=client.post(
        "/auth/login",data={
            "username":"test2", "password":"test2"
        }
    )

    assert response.status_code==200
    response_data = response.json()
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}


    res = client.get(f"/auth/users/{user_id}", headers=headers)  
    assert res.status_code == 200
    response_data = res.json()
    assert response_data["id"] == user_id
    assert response_data["username"] == "test2"
    assert response_data["email"] == "test2@gmail.com"


def test_update_user_by_id(client):
    #1st user signup as normol user
    signup_response=client.post(
        "/auth/signup/user",json={
            "username":"test3", "email":"test3@gmail.com", "password":"test3" })
    assert signup_response.status_code == 201
    signup_data= signup_response.json()
    user_id = signup_data["id"]
    
        #2nd suer login as admin
    signup_response2=client.post(
        "/auth/signup/admin",json={ "username":"test5",  "email":"test5@gmail.com","password":"test5"})
    assert signup_response2.status_code == 201
    signup_data= signup_response2.json()
    user_id_2=signup_data["id"]
   
    
    #login code 
    response=client.post(
        "/auth/login",data={
            "username":"test5",
            "password":"test5"  } )

    assert response.status_code==200
    response_data = response.json()
    access_token = response_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    update_res = client.put(f"/auth/users/{user_id}", headers=headers,json={
        "username":"test4", "email":"test4@gmail.com","password":"test1234" })  

    assert update_res.status_code == 200

def test_delete_user_by_id(client):
    #1st user signup as normol user
    signup_response=client.post(
        "/auth/signup/user",json={
            "username":"test12", "email":"test12@gmail.com", "password":"test6" })
    assert signup_response.status_code == 201
    signup_data= signup_response.json()
    user_id = signup_data["id"]
    
        #2nd suer login as admin
    signup_response2=client.post(
        "/auth/signup/admin",json={ "username":"test7",  "email":"test7@gmail.com","password":"test7"})
    assert signup_response2.status_code == 201
    signup_data= signup_response2.json()
    user_id_2=signup_data["id"]

    
    #login code - normol suer login and he can delete own their data
    response=client.post(
        "/auth/login",data={
            "username":"test7",
            "password":"test7"  } )

    assert response.status_code==200
    response_data = response.json()
    access_token = response_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    delete_user = client.delete(f"/auth/delete-users/{user_id}", headers=headers) 
    assert delete_user.status_code == 200



def test_batch_delete(client):
    #1st user signup as normol user
    signup_response=client.post(
        "/auth/signup/user",json={
            "username":"test11", "email":"test11@gmail.com", "password":"test11" })
    assert signup_response.status_code == 201
    signup_data= signup_response.json()
    user_id = signup_data["id"]
    
       #2nd suer login as normol user
    signup_response2=client.post(
        "/auth/signup/user",json={
            "username":"test7", "email":"test7@gmail.com", "password":"test7" })
    assert signup_response2.status_code == 201
    signup_data2= signup_response2.json()
    user_id2 = signup_data2["id"]

        #3rd suer login as admin
    signup_response3=client.post(
        "/auth/signup/admin",json={ "username":"test8",  "email":"test8@gmail.com","password":"test8"})
    assert signup_response3.status_code == 201
    signup_data3= signup_response3.json()

    
    #login code 
    response=client.post(
        "/auth/login",data={
            "username":"test8",
            "password":"test8"  } )

    assert response.status_code==200
    response_data = response.json()
    access_token = response_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    batch_delete_response = client.post(
        "/auth/batch-delete",
        headers=headers, 
        json={"user_ids": [user_id, user_id2]}  # Correctly send user IDs
    )
    assert batch_delete_response.status_code == 200
    # batch_delete_data = batch_delete_response.json()


def test_view_trash(client):
    signup_response=client.post(
        "/auth/signup/admin",json={
            "username":"demo", "email":"demo@gmail.com", "password":"demo" })
    assert signup_response.status_code == 201
    signup_data= signup_response.json()
    
    signup_response=client.post(
        "/auth/signup/user",json={
            "username":"test113", "email":"test193@gmail.com", "password":"test113" })
    assert signup_response.status_code == 201
    signup_data= signup_response.json()
    user_id = signup_data["id"]

    response=client.post(
        "/auth/login",data={
            "username":"demo", "password":"demo"
        })
    assert response.status_code==200
    response_data = response.json()
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    delete_user = client.delete(f"/auth/delete-users/{user_id}", headers=headers) 
    assert delete_user.status_code == 200

    res = client.get("/auth/view-trash", headers=headers)  
    assert res.status_code == 200


def test_restore_trash(client):
    signup_response=client.post(
        "/auth/signup/admin",json={
            "username":"admin12", "email":"test142@gmail.com", "password":"admin12" })
    assert signup_response.status_code == 201
    signup_data1= signup_response.json()
  
    signup_response2=client.post(
        "/auth/signup/user",json={
            "username":"test14", "email":"test14@gmail.com", "password":"test14" })
    assert signup_response2.status_code == 201
    signup_data2= signup_response2.json()
    user_id = signup_data2["id"]

    response=client.post(
        "/auth/login",data={
            "username":"admin12", "password":"admin12"
        })

    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    delete_user = client.delete(f"/auth/delete-users/{user_id}", headers=headers) 
    assert delete_user.status_code == 200

    restore_response = client.put(f"auth/restore-user/{user_id}", headers=headers)
    assert restore_response.status_code == 200
    assert restore_response.json()["message"] == "User restored successfully"


def test_permamently_delete(client):
    response=client.post(
        "/auth/signup/admin",json={
            "username":"test19", "email":"test122@gmail.com", "password":"test19" })
    assert response.status_code == 201
    res=client.post(
        "/auth/signup/user",json={
            "username":"test13", "email":"test13@gmail.com", "password":"test6" })
    assert res.status_code == 201
    signup_data= res.json()
    user_id = signup_data["id"]

    response=client.post(
        "/auth/login",data={"username":"test19", "password":"test19"})
    assert response.status_code==200
    response_data = response.json()
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    delete_user = client.delete(f"/auth/delete-users/{user_id}", headers=headers) 
    assert delete_user.status_code == 200

    permament_delete_res=client.delete(f"/auth/permamently-delete/{user_id}",headers=headers)
    assert permament_delete_res.status_code == 200
    assert permament_delete_res.json()["message"] == "User Permamently Deleted Successfully"


def test_permamently_delete_unauthorized(client):

    res=client.post(
        "/auth/signup/user",json={
            "username":"test", "email":"test@gmail.com", "password":"test" })
    assert res.status_code == 201
    signup_data= res.json()
    user_id = signup_data["id"]

    response=client.post(
        "/auth/login",data={"username":"test", "password":"test"})
    assert response.status_code==200
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    delete_user = client.delete(f"/auth/delete-users/{user_id}", headers=headers) 
    assert delete_user.status_code == 200

    permament_delete_res=client.delete(f"/auth/permamently-delete/{user_id}",headers=headers)
    assert permament_delete_res.status_code == 401       #unauthorized User try to delete