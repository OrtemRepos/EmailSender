from pydantic import BaseModel, EmailStr, Field


class UserEmail(BaseModel):
    email: EmailStr = Field(description="User email address", examples=["user@example.com"])
    token: str = Field(description="Access token", examples=["Xbh7BdJLQoBZ8O5xBhIRjoabK5QQmQCxgX4K4maJulzQQXycKiASFHGXh3d7JfQ9"])
