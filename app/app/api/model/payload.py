from pydantic import BaseModel

class Posts(BaseModel):
	title: str
	text: str

class Payload(BaseModel):
    payload: Posts | None