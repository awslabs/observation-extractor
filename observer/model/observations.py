import pydantic

class Thought(pydantic.BaseModel):
    title: str
    description: str
    evidence: str
    question: str

class Thoughts(pydantic.BaseModel):
    thoughts: list[Thought]

class Observation(pydantic.BaseModel):
    thought: Thought
    metadata: dict

class Observations(pydantic.BaseModel):
    observations: list[Observation]
