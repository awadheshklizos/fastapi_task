from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from beanie import PydanticObjectId
from app.models.user_model import User
from app.models.trash_model import Trash
from app.schemas.auth_schema import Token, LoginForm
from app.core.security import (authenticate_user, create_access_token,create_refresh_token,
    get_current_user,
    get_password_hash
)
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.schemas.user_schema import UserOut,UserCreate,UserListResponse,UserUpdate,BatchDeleteRequest
from app.core.database import init_db
from fastapi.responses import JSONResponse
from typing import Optional
from typing import List


router = APIRouter(tags=["auth"])




@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
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

    # Store the refresh token in the user's document
    user.refresh_tokens.append(refresh_token)
    await user.save()

    return {"access_token": access_token,"refresh_token":refresh_token,  "token_type": "bearer"}



@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
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
    )
    await user.insert()
    return user

@router.post("/refresh", response_model=Token)
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
        token_data = TokenData(username=username)
    except:
        raise credentials_exception

    user = await User.find_one(User.username == token_data.username)
    if not user or refresh_token not in user.refresh_tokens:
        raise credentials_exception

    # Generate a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # Optionally, issue a new refresh token
        "token_type": "bearer",
    }


@router.get("/users", response_model=UserListResponse)
async def get_all_users(current_user: User = Depends(get_current_user)):
    users = await User.find_all().to_list()
    return {"users": users}


@router.get("/users/{user_id}",response_model=UserOut)
async def get_user_by_id(user_id:PydanticObjectId,current_user:User=Depends(get_current_user)):
    user=await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


      #Update User data by their id ,only authorized and same loged in user can update
@router.put('/users/{user_id}', response_model=UserOut)
async def update_userdata_by_id(
    user_id: PydanticObjectId,
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
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


@router.delete('/users/{user_id}', response_model=UserOut)
async def soft_delete_user_by_id(
    user_id: PydanticObjectId,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can Delete only Your Own data ",
        )
    # Find the user to be soft-deleted
    user = await User.find_one(User.id == user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    dict_user=user.dict()
    dict_user['id']=current_user.id
# Move the user's record to the Trash collection
    trash_record = Trash(
        original_data=dict_user,
        deleted_by=dict_user['id'],
        reason=reason,
        delete_status=True
    )

    await trash_record.insert()
    await user.delete()
    return user


@router.delete('/users/multiple-delete', response_model=List[UserOut])
async def batch_soft_delete_users(
    batch_delete_request: BatchDeleteRequest,
    current_user: User = Depends(get_current_user)
    ):
    
    print("Batch delete triggered!") 
    
    valid_user_ids = []
    for uid in batch_delete_request.user_ids:
        try:
            valid_user_ids.append(PydanticObjectId(uid))
        except Exception:
            continue

    if not valid_user_ids:
        raise HTTPException(
            status_code=400,
            detail="No valid user IDs provided"
        )

    users = await User.find(In(User.id, valid_user_ids)).to_list()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found for deletion",
        )

    deleted_users = []
    for user in users:
        
        user_data = user.dict()
        user_data["id"] = user.id 

        trash_record = Trash(
            original_data=user_data, 
            deleted_by=current_user.id,  # Required field
            # reason=batch_delete_request.reason, 
        )
        await trash_record.insert()
        await user.delete()

        deleted_users.append(user)

    return deleted_users

