@router.get("/users/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    # Ensure only authenticated users can access this endpoint
    user = await User.find_one(User.id == user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user