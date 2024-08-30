from ninja import Schema
from typing import Optional

class MenuSchema(Schema):
    parent_id: Optional[int] = None
    name: str
    url: str
    icon: str
    sequence: int