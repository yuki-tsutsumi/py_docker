from pydantic import BaseModel,Field, validator
from typing import Optional

class Plus(BaseModel):
	a: Optional[int] = Field(..., ge=0, le=100)
	b: Optional[int] = Field(..., ge=0, le=100)
