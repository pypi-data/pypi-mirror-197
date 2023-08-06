from pydantic import BaseModel, Field
from typing import List, Dict


class TaskConfigurationSchema(BaseModel):
    task_input: List[Dict] = Field(title="task_input",
                                   description="The input for the task",
                                   default=[])
    detail: List[Dict] = Field(title="detail",
                               description="Details pertaining to the task",
                               default=[])
