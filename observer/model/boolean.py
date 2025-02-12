from pydantic import BaseModel


class Boolean(BaseModel):
    result: bool

class Booleans(BaseModel):
    results: list[bool]