from pydantic import BaseModel,EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "user" 
    disabled: bool = False

class UserInDB(User):
    hashed_password: str

class EmailSchema(BaseModel):
    username: str
    email: EmailStr

