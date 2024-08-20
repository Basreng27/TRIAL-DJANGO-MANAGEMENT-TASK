from ninja import Schema
from datetime import date
from typing import Optional

class TaskSchema(Schema):
    title: str
    description: str
    project_id: int
    assigned_user_id: int
    status: str
    priority: str
    due_date: date
    created_at: Optional[date] = None
    updated_at: Optional[date] = None