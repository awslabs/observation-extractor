import pydantic
from datetime import datetime

class Thought(pydantic.BaseModel):
    title: str
    document_date: datetime
    document_type: str
    description: str
    evidence: str
    question_number: int
    question: str

class Thoughts(pydantic.BaseModel):
    thoughts: list[Thought]

class Observation(pydantic.BaseModel):
    thought: Thought
    metadata: dict

    def to_dict(self):
        return {
            'title': self.thought.title,
            'document_date': str(self.document_date),
            'document_type': self.document_type,
            'description': self.thought.description,
            'evidence': self.thought.evidence,
            'question_number': self.question_number,
            'question': self.thought.question,
            'metadata': self.metadata
        }

class Observations(pydantic.BaseModel):
    observations: list[Observation]
