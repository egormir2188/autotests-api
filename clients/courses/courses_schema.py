from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from clients.users.users_schema import UserSchema
from clients.files.files_schema import FileSchema
from tools.fakers import fake


class ShortCourseSchema(BaseModel):
    """
    Краткое описание сущности Course.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(default_factory=fake.max_score)
    min_score: int = Field(default_factory=fake.min_score)
    description: str = Field(default_factory=fake.sentence)
    estimated_time: str = Field(default_factory=fake.estimated_time)


class CourseSchema(ShortCourseSchema):
    """
    Описание структуры курса.
    """
    id: str
    preview_file: FileSchema
    created_by_user: UserSchema

class CreateCourseRequestSchema(ShortCourseSchema):
    """
    Описание структуры запроса для создания курса.
    """
    preview_file_id: str = Field(default_factory=fake.uuid4)
    created_by_user_id: str = Field(default_factory=fake.uuid4)

class CreateCourseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """
    course: CourseSchema

class GetCoursesQuerySchema(BaseModel):
    """
    Описание стрктуры запроса для получения списка курсов.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    user_id: str

class GetCoursesResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение списка курсов.
    """
    courses: list[CourseSchema]

class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на частичное обновление данных пользователя.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(default_factory=fake.max_score)
    min_score: int | None = Field(default_factory=fake.min_score)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(default_factory=fake.estimated_time)

class UpdateCourseResponseSchema(BaseModel):
    """
    Описание структуру ответа чистичного обновления курса (полность наследуется от CourseSchema)
    """
    course: CourseSchema