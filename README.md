**#FastAPI Application with JWT Authentication, Soft-Deletion, and Restore and Various Feature**

**FastAPI-based API** This is a sample FastAPI project that demonstrates how to integrate FastAPI with MongoDB for handling RESTful APIs. Like Create user , login , Delete and Restore with Admin and Normol user Restriction


  ## Table of Contents
- [Feature] 
- [Installation](#installation)
- [Usage](#usage)
- [Testing]

## Features

- **User SignUP**
- **User login (JWT Authentication)**
- **CRUD operations** (Create, Read, Update, Delete)
- **User Restriction for Performing operation** (admin role and Normol user)
- **User can upload image**
- **Two Collection user and Trash-using MongoDb**
- **Soft-delete and restore users**
- **Permanent delete from trash**

**A Brief Description of Feature**
  1. User can Signup using two Different Route ,  if a normol user then go to auth/signup/user route and fill their details and got Registered but if its an admin then go to admin route auth/signup/admin for registration
  2. A Normol user can have a limited Access to perform their own data manipulation(CRUD) but they can not permament delete itself & Admin can perform Entire Crud Operation with all Data
  3. User can Login Using their username and password then he got the access Token and Refresh Token , Access token validity for 30 min and Refresh Token have 7 day
  4. There are Separate Role for user and Admin ,Both have own Access Right.
  5. User( Normol user/ admin) can Uplaod their Profile picture(img only) using the route and it got update in User data
  6. There are Two colletion Users and Trash - I am using MongoDb for Storing data Locally , Trash can store soft Deleted data of users
  7. There are Two Option for Deletion Soft Deletion and Permament Deletion - soft deletion can Perform by Any User but Permament deletion can only perform Admin
     
  


## Getting started [installation Process]

Follow these steps to set up the project locally:

## Clone the repository
- Simple Create a Dir and go inside it and just Run this Command- 
- **bash:** git clone https://github.com/awadheshklizos/fastapi_task.git

- check your Current Directory , if you are inside any other Directory then Come out to Root Directory


## Setup a virtual enviroment

- **bash**
-  **Run:** python -m venv .venv
-  **For macOS/Linux:** source .venv/bin/activate
-  **For Windows:** .venv\Scripts\activate    
-  **For Windows:** - .\venv\Scripts\activate   (if first one is not worked for activate)

**##Database-** 
- Make Sure you have MongoDb Database in your System with Setup
- 
## Install dependencies

- **bash**
  - python -m pip install --upgrade pip
  - pip install -r requirements.txt

## Run the application:
type this Command in your termial ( Env should be Activated)
- **uvicorn app.main:app --reload**
  
- in Case not Run the port and not able to see any Result just change the port  -  **uvicorn app.main:app --port 8001**


**Your application will be available at [http://127.0.0.1:8000].**

## API Endpoints

- ## Root Route

  - **Try accessing the root route:** `http://127.0.0.1:8000`
    - This will return a JSON response:
      ```json
      {
       "message": "FoR Test the code "
      }
      ```
- **Switch to FastAPI Docs page**
-   http://127.0.0.1:8000/**docs**   (just write **/docs** at end of the url)

**Lets Discuss about Various Route-**

- ## Authentication Route 
  - **POST /login: Login and get JWT token.**
    -   {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0MDA2ODExN30.pCHcaQHc-vTa0mjUeb50i3ChF6AnFyA4W3F6BOaopHE",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0MDY3MTExN30.5E5k3p8Nc540wgJGtFkOQdlz3PXxMm0C7MTxJPFjoCA",
      "token_type": "bearer"
    }
  - **POST auth/signup/user: Register a Normol user.**
  - **POST auth/signup/admin: Register an Admin.**
  - **POST auth/refresh/{refresh_token}: Regenerate the Access Token.**
  
- ## Users and Admin
  - **GET  auth/users/: Get all users** (admin only).
  -      {
            "users": [
              {
                "username": "user",
                "email": "e@example.com",
                "id": "67b6edb85627d21d68ca5904",
                "created_at": "2025-02-20T14:24:16.716000",
                "role": "user"
              },
              {
                "username": "admin",
                "email": "admin@example.com",
                "id": "67b6edcb5627d21d68ca5905",
                "created_at": "2025-02-20T14:24:35.421000",
                "role": "admin"
              }
            ]
          }
  - **GET auth/users/<user_id>:** Get user by ID (normol user can Get only their own Data but admin can view all user data through their id).
  -       {
          "username": "user",
          "email": "e@example.com",
          "id": "67b6edb85627d21d68ca5904",
          "created_at": "2025-02-20T14:24:16.716000",
          "role": "user"
        }
      
  - **PUT auth/users/<user_id>:** Update user (Normol user can update only their own data but Admin can have access to update any user data).
  - **DELETE auth/delete-users/<user_id>:** Soft-delete user (a regular user can delete ownself but admin can delete any user).
  - **POST auth/batch-delete:** Soft-delete multiple users (Admin only , a normol user can not do this).
  - **GET auth/view-trash:** View soft-deleted users (admin only).
  - **PUT auth/restore-user/<user_id>:** Restore soft-deleted user (admin only).
  - **DELETE auth/permamently-delete/<user_id>:** Permanently delete from trash (admin only).
  - **POST auth/upload-profile-picture:** set a Profile picture ( admin and user both can set own picture)
  - 
  - **GET /Read Root:** Root page


## Testing

- To run tests for this application, use pytest:

- bash:
  
**  python -m pytest**
