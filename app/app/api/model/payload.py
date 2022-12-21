from pydantic import BaseModel,Field, validator
from typing import Optional

class Posts(BaseModel):
	title: str = Field(..., min_length=2, max_length=10) #titleは2文字以上10文字以下でなければならない
	text: Optional[int] = Field(..., ge=2, le=10) #textは整数でかつ2以上10以下でなければならない
	
	@validator("text")
	def validate_hoge(cls, value):
		if value is 5: #textは5だけ使用不可
			raise TypeError("5 is disabled") 
		return value


class Payload(BaseModel):
    payload: Posts