from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserLogin, Token, UserResponse
from app.services.auth import (
    authenticate_user, create_access_token, 
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.services.auth import verify_password, get_password_hash
from app.models.user import User

router = APIRouter()

@router.post("/login/{org_id}", response_model=Token)
async def login_for_access_token(org_id: str, form_data: UserLogin):
    user = await authenticate_user(form_data.email, form_data.password, org_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "org_id": org_id}, 
        expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role,
        organization_id=user.organization_id,
        is_active=user.is_active,
        created_at=user.created_at
    )
    
    return Token(
        access_token=access_token, 
        token_type="bearer",
        user=user_response
    )

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        organization_id=current_user.organization_id,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user)
):
    
    
    if not verify_password(current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    current_user.password = get_password_hash(new_password)
    await current_user.save()
    
    return {"message": "Password updated successfully"}


@router.get("/me/with-org")
async def read_users_me_with_org(current_user: User = Depends(get_current_active_user)):
    from app.models.organization import Organization
    
    organization = await Organization.get(current_user.organization_id)
    
    user_response = UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        organization_id=current_user.organization_id,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )
    
    return {
        "user": user_response,
        "organization": {
            "id": str(organization.id),
            "name": organization.name,
            "description": organization.description
        } if organization else None
    }