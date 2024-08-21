from ninja import Schema
from datetime import date
from typing import Optional

class LabelSchema(Schema):
    name: str
    color: str
    created_at: Optional[date] = None
    updated_at: Optional[date] = None