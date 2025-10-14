from pydantic import BaseModel, Field
import uuid

class Supplement(BaseModel):
  id: uuid.UUID = Field(default_factory=uuid.uuid4)
  name: str = Field(..., description="Name of supplement")
  
