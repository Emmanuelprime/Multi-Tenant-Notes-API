from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationCreate
from app.services.auth import get_password_hash
from bson import ObjectId

class OrganizationService:
    @staticmethod
    async def create_organization_with_admin(organization_data: OrganizationCreate):
        try:
            # Create organization first
            organization = Organization(
                name=organization_data.name,
                description=organization_data.description
            )
            await organization.insert()
            
            # Create admin user for this organization
            admin_user = User(
                email=organization_data.admin_email,
                password=get_password_hash(organization_data.admin_password),
                name=organization_data.admin_name,
                role="admin",
                organization_id=str(organization.id)
            )
            await admin_user.insert()
            
            return organization, admin_user
        except Exception as e:
            # Clean up organization if user creation fails
            if 'organization' in locals():
                await organization.delete()
            raise e
    
    @staticmethod
    async def get_organization(org_id: str):
        
        try:
            obj_id = ObjectId(org_id)
        except Exception:
            return None
        return await Organization.get(obj_id)