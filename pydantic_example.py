from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = Field(alias='isActive')

user = User(id=1,
            name='Alice',
            email='test@test.ru',
            is_active=False,
            )
print(user.model_dump_json())