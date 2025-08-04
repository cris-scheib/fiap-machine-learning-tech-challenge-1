from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str

    class Config:
        from_attributes = True