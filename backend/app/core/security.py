from fastapi import Header, HTTPException


ROLE_ADMIN = "admin"
ROLE_STAFF = "postal_staff"
ROLE_CUSTOMER = "customer"


def require_role(required_roles: set[str]):
    async def _verify_role(x_role: str | None = Header(default=None)):
        if x_role is None:
            raise HTTPException(status_code=401, detail="Missing role header")
        if x_role not in required_roles:
            raise HTTPException(status_code=403, detail="Role not permitted")
        return x_role

    return _verify_role
