# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import pydantic
from datetime import datetime

class Thought(pydantic.BaseModel):
    title: str
    document_date: datetime | None
    document_type: str | None
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
            'document_date': str(self.thought.document_date),
            'document_type': self.thought.document_type,
            'description': self.thought.description,
            'evidence': self.thought.evidence,
            'question_number': self.thought.question_number,
            'question_set': self.metadata['question_set'],
            'question': self.thought.question,
            'metadata': self.metadata
        }

class Observations(pydantic.BaseModel):
    observations: list[Observation]
