from ninja import Schema

class TaskLabelSchema(Schema):
    task_id: int
    label_id: int