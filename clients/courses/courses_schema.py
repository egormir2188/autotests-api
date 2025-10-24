from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from clients.users.users_schema import UserSchema
from clients.files.files_schema import FileSchema


class ShortCourseSchema(BaseModel):
    """
    Краткое описание сущности Course.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str
    max_score: int
    min_score: int
    description: str
    estimated_time: str


class CourseSchema(ShortCourseSchema):
    """
    Описание структуры курса.
    """
    id: str
    preview_file: FileSchema
    created_by_user: UserSchema


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

class CreateCourseRequestSchema(ShortCourseSchema):
    """
    Описание структуры запроса для создания курса.
    """
    preview_file_id: str
    created_by_user_id: str

class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на частичное обновление данных пользователя.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str | None
    max_score: int | None
    description: str | None
    estimated_time: str | None

class UpdateCourseResponseSchema(CourseSchema):
    """
    Описание структуру ответа чистичного обновления курса (полность наследуется от CourseSchema)
    """
    pass