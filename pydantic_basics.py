"""
{
  "course": {
    "id": "string",
    "title": "string",
    "maxScore": 0,
    "minScore": 0,
    "description": "string",
    "previewFile": {
      "id": "string",
      "filename": "string",
      "directory": "string",
      "url": "https://example.com/"
    },
    "estimatedTime": "string",
    "createdByUser": {
      "id": "string",
      "email": "user@example.com",
      "lastName": "string",
      "firstName": "string",
      "middleName": "string"
    }
  }
}
"""

import uuid

from pydantic import BaseModel, Field, ConfigDict, computed_field, HttpUrl, EmailStr
from pydantic.alias_generators import to_camel

from tools.fakers import fake


class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl

class UserSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias='lastName')
    first_name: str = Field(alias='firstName')
    middle_name: str = Field(alias='middleName')

    @computed_field
    def username(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_user_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

class CourseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = 'Playwright'
    max_score: int = Field(alias='maxScore', default=1000)
    min_score: int = Field(alias='minScore', default=100)
    description: str = 'Playwright course'
    preview_file: FileSchema
    estimated_time: str = Field(alias='estimatedTime', default='2 week')
    created_by_user: UserSchema

course_default_model = CourseSchema(
    id='course-id',
    title='Playwright',
    max_score=100,
    min_score=10,
    description='Playwright',
    preview_file=FileSchema(
        id= 'file_id',
        filename='file.png',
        directory='testdata',
        url='https://example.com/'
    ),
    estimated_time='1 week',
    created_by_user=UserSchema(
        id='user_id',
        email=fake.email(),
        last_name='name',
        first_name='name1',
        middle_name='name2'
    )
)

print('Course default model:', course_default_model)

course_dict = {
    "id": "course-id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "description": "Playwright",
    "previewFile": {
          "id": "string",
          "filename": "string",
          "directory": "string",
          "url": "https://example.com/"
    },
    "estimatedTime": "1 week",
    "createdByUser": {
          "id": "string",
          "email": "user@example.com",
          "lastName": "string",
          "firstName": "string",
          "middleName": "string"
    }
}

course_dict_model = CourseSchema(**course_dict)
print('Course dict model:', course_default_model)

course_json = """
{
    "id": "course-id",
    "title": "Playwright",
    "maxScore": 100,
    "minScore": 10,
    "description": "Playwright",
    "previewFile": {
          "id": "string",
          "filename": "string",
          "directory": "string",
          "url": "https://example.com/"
    },
    "estimatedTime": "1 week",
    "createdByUser": {
          "id": "string",
          "email": "user@example.com",
          "lastName": "string",
          "firstName": "string",
          "middleName": "string"
    }
}
"""
course_json_model = CourseSchema.model_validate_json(course_json)
print('Course JSON model:', course_json_model)
print(course_json_model.model_dump())
print(course_json_model.model_dump_json(by_alias=True))

# course1 = CourseSchema()
# course2 = CourseSchema()
# print(course1.id)
# print(course2.id)