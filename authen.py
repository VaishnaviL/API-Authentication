from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models import TokenData, UserInDB, User
from database import get_user
from utils import SECRET_KEY, ALGORITHM

# OAuth2PasswordBearer defines the token URL endpoint for authentication.
# FastAPI will expect the token to be passed in the Authorization header as "Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Get the current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Custom exception to raise if credentials are invalid
        credentials_exception = HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode the JWT token using the secret key and algorithm
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            role = payload.get("role")

            # If either username or role is missing, reject the request
            if username is None or role is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        # Fetch the user from database (based on username extracted from token)
        user = get_user(username=username)
        if user is None:
            raise credentials_exception

        user.role = role  # attach role from token
        return user
    except Exception as e:
        print("Error in get_current_user()",e)


def get_current_active_user( current_user: UserInDB = Depends(get_current_user)):
    # If user is disabled/inactive, block access
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# authorization 
def require_admin(current_user: User = Depends(get_current_user)):
    # If user is not admin, deny access

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

#Role-based access decorator
def require_roles(allowed_roles: list[str]):
    """
    Returns a dependency that checks whether the current user's role is in the allowed list.
    Useful for endpoints that allow multiple roles (e.g., admin, auditor).
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return current_user
    return role_checker
    
# print("authen loaded sucess")
# print("Functions defined:", dir())
