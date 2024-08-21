from ninja import Schema

class TaskCategorySchema(Schema):
    task_id: int
    category_id: int