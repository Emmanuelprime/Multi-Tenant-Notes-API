from fastapi import APIRouter, HTTPException, Depends,status
from typing import List
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService
from app.services.auth import get_current_active_user
from app.models.user import User

router = APIRouter()

def require_admin(user: User):
    """Check if user has admin role"""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required for this operation"
        )

@router.post("/", response_model=UserResponse)
async def create_user(
    org_id: str,
    user_data: UserCreate,
    current_user: User = Depends(get_current_active_user)
):
    require_admin(current_user)
    
    if current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        user = await UserService.create_user(user_data, org_id)
        return UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role,
            organization_id=user.organization_id,
            is_active=user.is_active,
            created_at=user.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[UserResponse])
async def get_organization_users(
    org_id: str,
    current_user: User = Depends(get_current_active_user)
):
    require_admin(current_user)
    
    if current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    users = await UserService.get_organization_users(org_id)
    return [
        UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role,
            organization_id=user.organization_id,
            is_active=user.is_active,
            created_at=user.created_at
        ) for user in users
    ]

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_role(
    org_id: str,
    user_id: str,
    user_update: dict,  # Expecting {"role": "new_role"}
    current_user: User = Depends(get_current_active_user)
):
    require_admin(current_user)
    
    if current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if user_id == str(current_user.id):
        raise HTTPException(
            status_code=400, 
            detail="Cannot modify your own role"
        )
    
    user = await UserService.get_user_by_id(user_id, org_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user role
    new_role = user_update.get("role")
    if new_role not in ["reader", "writer", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    user.role = new_role
    await user.save()
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role,
        organization_id=user.organization_id,
        is_active=user.is_active,
        created_at=user.created_at
    )

@router.delete("/{user_id}")
async def delete_user(
    org_id: str,
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    require_admin(current_user)
    
    if current_user.organization_id != org_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if user_id == str(current_user.id):
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete your own account"
        )
    
    user = await UserService.get_user_by_id(user_id, org_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    return {"message": "User deleted successfully"}