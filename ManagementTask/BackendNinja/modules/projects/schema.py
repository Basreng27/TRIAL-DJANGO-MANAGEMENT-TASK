from ninja import Schema
from datetime import date
from typing import Optional

class ProjectSchema(Schema):
    user_id: int
    name: str
    description: str
    created_at: Optional[date] = None
    updated_at: Optional[date] = None