from typing import Any,Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    message:str
    status:str
    data:Optional[Any]