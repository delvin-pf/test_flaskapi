from pydantic import BaseModel, Field


class WebHookSchema(BaseModel):
	"""
	Attributes:
		name: str
		email: str
		status: str
		valor: float
		forma_pagamento: str
		parcelas: int
	"""
	
	nome: str = Field()
	email: str = Field()
	status: str = Field()
	valor: float = Field()
	forma_pagamento: str = Field()
	parcelas: int = Field()
 
	