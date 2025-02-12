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

    def to_dict(self):
        return {
            'title': self.thought.title,
            'description': self.thought.description,
            'evidence': self.thought.evidence,
            'question': self.thought.question,
            'metadata': self.metadata
        }

class Observations(pydantic.BaseModel):
    observations: list[Observation]
