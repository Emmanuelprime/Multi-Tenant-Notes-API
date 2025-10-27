from fastapi import APIRouter, HTTPException, status
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.services.organization import OrganizationService

router = APIRouter()

@router.post("/", response_model=OrganizationResponse)
async def create_organization(organization_data: OrganizationCreate):
    organization, admin_user = await OrganizationService.create_organization_with_admin(organization_data)
    
    return OrganizationResponse(
        id=str(organization.id),
        name=organization.name,
        description=organization.description,
        admin_user={
            "id": str(admin_user.id),
            "email": admin_user.email,
            "name": admin_user.name,
            "role": admin_user.role
        },
        created_at=organization.created_at,
        updated_at=organization.updated_at
    )

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: str):
    organization = await OrganizationService.get_organization(org_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Get the admin user for this organization
    from app.models.user import User
    admin_user = await User.find_one({
        "organization_id": org_id, 
        "role": "admin"
    })
    
    return OrganizationResponse(
        id=str(organization.id),
        name=organization.name,
        description=organization.description,
        admin_user={
            "id": str(admin_user.id),
            "email": admin_user.email,
            "name": admin_user.name,
            "role": admin_user.role
        } if admin_user else None,
        created_at=organization.created_at,
        updated_at=organization.updated_at
    )