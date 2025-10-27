from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import get_password_hash
from bson import ObjectId

class UserService:
    @staticmethod
    async def create_user(user_data: UserCreate, organization_id: str):
        existing_user = await User.find_one({
            "email": user_data.email, 
            "organization_id": organization_id
        })
        if existing_user:
            raise ValueError("User with this email already exists in organization")

        pw_bytes = user_data.password.encode("utf-8") if user_data.password is not None else b""
        if len(pw_bytes) > 72:
            raise ValueError(
                "Password is too long for bcrypt (greater than 72 bytes). "
                "Use a shorter password (<=72 bytes) or truncate before sending."
            )

        user_dict = user_data.dict()
        user_dict["password"] = get_password_hash(user_data.password)
        user_dict["organization_id"] = organization_id
        
        user = User(**user_dict)
        return await user.insert()
    
    @staticmethod
    async def get_user_by_id(user_id: str, organization_id: str):

        
        try:
            obj_id = ObjectId(user_id)
        except Exception:
            return None
        return await User.find_one({"_id": obj_id, "organization_id": organization_id})
    
    @staticmethod
    async def get_organization_users(organization_id: str):
        return await User.find({"organization_id": organization_id}).to_list()