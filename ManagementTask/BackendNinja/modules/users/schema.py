from ninja import Schema
from typing import Optional

class UserSchema(Schema):
    username: str
    password: Optional[str] = None
    first_name: str
    last_name: str
    email: str