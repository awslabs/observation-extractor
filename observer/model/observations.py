import pydantic

class Thought(pydantic.BaseModel):
    title: str
    data: str

class Observation(pydantic.BaseModel):
    thought: Thought
    metadata: dict
