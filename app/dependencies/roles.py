from fastapi import Depends, HTTPException, status

from app.models.user import User
from app.routers.users import get_current_user


def require_role(*allowed_roles):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker


def admin_required():
    return require_role("ADMIN")


def organizer_required():
    return require_role("ORGANIZER")


def customer_required():
    return require_role("CUSTOMER")