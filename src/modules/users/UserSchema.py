from pydantic import BaseModel, Field


class UserSchema(BaseModel):
	"""
	Attributes:
		name: str
		email: str
		password: str
		token: str
	"""
	name: str = Field()
	email: str = Field()
	password: str = Field()
	token: str = Field()


class UserLoginSchema(BaseModel):
	"""
	Attributes:
		email: str
		password: str
	"""
	email: str = Field()
	password: str = Field()