from ninja import Schema
from datetime import date
from typing import Optional

class CategorySchema(Schema):
    name: str
    description: str
    created_at: Optional[date] = None
    updated_at: Optional[date] = None