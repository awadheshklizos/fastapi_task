from fastapi import FastAPI, File, UploadFile, HTTPException, status,APIRouter, Depends
from pathlib import Path
from datetime import datetime
from bson import ObjectId 
from jose import JWTError, jwt
import shutil
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from beanie import PydanticObjectId

from app.models.user_model import User
from app.models.trash_model import Trash
from app.schemas.auth_schema import Token, LoginForm,RegenerateToken
from app.core.security import (authenticate_user, create_access_token,create_refresh_token,
    get_current_user,
    get_password_hash)
from app.core.config import settings
from app.schemas.user_schema import UserOut,UserCreate,UserListResponse,UserUpdate,BatchDeleteRequest,TrashRecordResponse,TrashList,RestoreUser
from fastapi.responses import JSONResponse
from typing import Optional,List 





router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
async def login(login_request: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(login_request.username, login_request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(days=7)  # Refresh token lasts 7 days
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    user.refresh_tokens=refresh_token
    await user.save()

    return {"access_token": access_token,"refresh_token":refresh_token,  "token_type": "bearer"}


@router.post("/signup/user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    existing_user = await User.find_one({"$or": [{"username": user_data.username}, {"email": user_data.email}]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role='user'
    )

    await user.insert()
    return user


@router.post("/signup/admin", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(admin_data: UserCreate):
    existing_user = await User.find_one({"$or": [{"username": admin_data.username}, {"email": admin_data.email}]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )
    hashed_password = get_password_hash(admin_data.password)
    user = User(
        username=admin_data.username,
        email=admin_data.email,
        hashed_password=hashed_password,
        role='admin'
    
    )
    await user.insert()
    return user


@router.post("/refresh/{refresh_token}", response_model=RegenerateToken)
async def refresh_token(refresh_token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:

        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception
        
    except:
        raise credentials_exception

    user = await User.find_one(User.username == username)
    user_token=user.refresh_tokens
 
    if not user or user_token != refresh_token :
        raise credentials_exception

    # Generate a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires

    )
    return {
        "access_token": access_token,
    }


@router.get("/users", response_model=UserListResponse)
async def get_all_users(current_user: User = Depends(get_current_user)):
    # print(current_user.role)
    if current_user.role == 'admin':
        users = await User.find_all().to_list()
        return {"users": users}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You Have Not Access To View all Users! -  Only admin Can do This",
        ) 

@router.get("/users/{user_id}",response_model=UserOut)
async def get_user_by_id(user_id:PydanticObjectId,current_user:User=Depends(get_current_user)):
    user=await User.find_one(User.id == user_id)   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if current_user.role == 'user':
        if current_user.id==user_id:
            return user
        else:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You Can View Only your Data",
        )
    else:
        return user


      #Update User data by their id ,only authorized and same loged in user can update
@router.put('/users/{user_id}', response_model=UserOut)
async def update_userdata_by_id(
    user_id: PydanticObjectId,
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
): 
    if current_user.role == 'user':
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own data",
            )
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
 
    # Update the user data
    update_dict = update_data.dict(exclude_unset=True)  # Exclude fields that are not provided
    if "password" in update_dict:
        update_dict["hashed_password"] = get_password_hash(update_dict.pop("password"))
    await user.update({"$set": update_dict})
    updated_user = await User.find_one(User.id == user_id)
    return updated_user



@router.delete('/delete-users/{user_id}', response_model=UserOut)
async def soft_delete_user_by_id(
    user_id: PydanticObjectId,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    if current_user.role=='user':
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can Delete only Your Own data ",
            )
    # Find the user to be soft-deleted
    user = await User.find_one(User.id == user_id)
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_delete_status_check = await User.find_one({"_id": user_id, "delete_status": True})
    user_check_in_trash= await Trash.find_one({"original_data.id": ObjectId(user_id)})

    if user_check_in_trash:
        raise HTTPException(
            status_code=500,
            detail="User Already Present in Trash",
        )
    elif not user_check_in_trash and user_delete_status_check:
        raise HTTPException(
            status_code=400,
            detail="User Already Permamently Deleted.."
        )   
    dict_user=user.dict()
    # dict_user['id']=current_user.id
    print(current_user.id)

# Move the user's record to the Trash collection
    trash_record = Trash(
        original_data=dict_user,
        deleted_by=current_user.id,
        reason=reason,
        delete_status=True
    )

    await trash_record.insert()
    await user.update({"$set":{"delete_status":True}})
    return user



@router.post('/batch-delete',status_code=status.HTTP_200_OK)
async def batch_soft_delete_users(
    batch_delete_request: BatchDeleteRequest,
    current_user: User = Depends(get_current_user),
):

    if current_user.role=='user':
        raise HTTPException(
            status_code=403,
            detail='Only Admin Can Delete Multiple Records'
        ) 

    valid_user_ids = []
    for uid_str in batch_delete_request.user_ids:
        try:
            valid_user_ids.append(PydanticObjectId(uid_str))
        except Exception:
            continue

    if not valid_user_ids:
        raise HTTPException(
            status_code=400,
            detail="No valid user IDs provided"
        )
    already_deleted_user=list()    
    deleted_users_data = []
    users_not_found = []
    for user_id in valid_user_ids:
        user = await User.find_one(User.id == user_id) 
        if not user:
            users_not_found.append(str(user_id))
            continue
        user_data = user.dict()
        user_delete_status_check = await User.find_one({"_id": user_id, "delete_status": True})
        user_check_in_trash= await Trash.find_one({"original_data.id": ObjectId(user_id)})

        if user_check_in_trash:
            already_deleted_user.append(str(user_id))
            continue

        elif not user_check_in_trash and user_delete_status_check:
            already_deleted_user.append(str(user_id))
            continue
        # Create trash record
        trash_record = Trash(
            original_data=user_data,
            deleted_by=current_user.id,
            deletion_timestamp=datetime.now(),
            reason=batch_delete_request.reason,
            delete_status=True  )
        await trash_record.insert()
        await user.update({"$set":{"delete_status":True}})
        deleted_users_data.append(user_data)
    response = {
        "deleted_users": deleted_users_data,
        "already_deleted_user":already_deleted_user,
        "message": f"Successfully deleted {len(deleted_users_data)} users"
    }
    if users_not_found:
        response["warning"] = f"Users not found: {', '.join(users_not_found)}"

    if not deleted_users_data:
        raise HTTPException(
            status_code=404,
            detail="No users were deleted"
        )
    return response
    
#for converting the objectid to srting
def convert_objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


@router.get('/view-trash', response_model=TrashList)
async def view_trash(
    current_user: User = Depends(get_current_user),): 
    if current_user.role=='user':
        raise HTTPException(
            status_code=403,
            detail="You Have Not Access To View Trash Data"
        )
    trash_records = await Trash.find().to_list()

    if not trash_records:
        raise HTTPException(
            status_code=404,
            detail="No soft-deleted user records found"
        )

    formatted_records = []
    for record in trash_records:

        original_data = {k: convert_objectid_to_str(v) for k, v in record.original_data.items()}
        deleted_by = convert_objectid_to_str(record.deleted_by)
        deletion_timestamp = record.deletion_timestamp.strftime('%Y-%m-%d %H:%M:%S')  

        formatted_record = TrashRecordResponse(
            id=str(record.id), 
            original_data=original_data,
            deletion_timestamp=deletion_timestamp,
            deleted_by=deleted_by,
            reason=record.reason,
            delete_status=True,  
        )
        formatted_records.append(formatted_record)
    return TrashList(trash=formatted_records)



@router.put('/restore-user/{user_id}')
async def restore_user_data(
    # restore_data: RestoreUser,
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    if current_user.role=='user':
        raise HTTPException(
            status_code=403,
            detail="Only Admin can Restore the Trash Record"
        )
    trash_record = await Trash.find_one({"original_data.id": ObjectId(user_id)})
    if not trash_record:
        raise HTTPException(
            status_code=404,
            detail="No soft-deleted user record found"
        )
    try:
        original_data = trash_record.original_data
        res= str(original_data.get('id'))

        update_result = await User.find_one({"_id": original_data.get('id')}).update(
            {"$set": {"delete_status": False}}
        )
    
        await Trash.find({"_id": trash_record.id}).delete()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error restoring user: {str(e)}"
        )

    return {
        "status": "success",
        "message": "User restored successfully",
        "restored_user_id": res
    }

@router.delete('/permamently-delete/{user_id}',status_code=status.HTTP_200_OK)
async def permamently_delete_user_by_id(
    user_id:str,
    current_user:User=Depends(get_current_user)
):
    if current_user.role=='user':
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    trash_record = await Trash.find_one({"original_data.id": ObjectId(user_id)})
    if not trash_record:
        raise HTTPException(
            status_code=404,
            detail="No User found for Permamently Deletion")
    try:
        original_data=trash_record.original_data
        response=str(original_data.get('id'))

        await Trash.find({"_id":trash_record.id}).delete()
    except:
        raise HTTPException(
            status_code=500,
            detail="Error during Deletion of Data"
        )    
    return {
        "message":"User Permamently Deleted Successfully",
        'delete_user_id':response
    }    


#for upload profile picture in local storage , create dir within current path
UPLOAD_DIR = Path("uploads/profiles")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-profile-picture/")
async def upload_profile_picture(file: UploadFile = File(),current_user:User=Depends(get_current_user)):
    username=current_user.username

    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Please upload an image.",
            )
        
        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_path = rf"assignment\uploads\profiles\{file.filename}"

        update_result = await User.find_one({"username":username}).update(
            {"$set": {"profile_picture": file_path}}
        )

        return {"message": f"Profile picture uploaded successfully.", "file_path": str(file_path)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while uploading the file: {str(e)}",
        )
