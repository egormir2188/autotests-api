from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from tools.fakers import fake


class ShortExerciseSchema(BaseModel):
    """
    Короткое описание сущности Exerxise.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    max_score: int = Field(default_factory=fake.max_score)
    min_score: int = Field(default_factory=fake.min_score)
    order_index: int = Field(default_factory=fake.integer)
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(default_factory=fake.estimated_time)

class ExerciseSchema(ShortExerciseSchema):
    """
    Описание структуры задания.
    """
    id: str
    course_id: str

class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса для получения списка заданий курса.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    course_id: str

class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка заданий
    """
    exercises: list[ExerciseSchema]

class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания/получения/обновлении задания
    """
    exercise: ExerciseSchema


class CreateExerciseRequestSchema(ShortExerciseSchema):
    """
    Описание структуры запроса для создания задания.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    course_id: str = Field(default_factory=fake.uuid4)


class CreateExerciseResponseSchema(GetExerciseResponseSchema):
    """
    Описание структуры ответа создания задания (полностью наследуется от GetExerciseResponseDict).
    """
    pass

class UpdateExerciseRequestSchema(ShortExerciseSchema):
    """
    Описание структуры запроса для обновления задания.
    """
    title: str | None = Field(default_factory=fake.sentence)
    max_score: int | None = Field(default_factory=fake.max_score)
    min_score: int | None = Field(default_factory=fake.min_score)
    order_index: int | None = Field(default_factory=fake.integer)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(default_factory=fake.estimated_time)

class UpdateExerciseResponseSchema(GetExerciseResponseSchema):
    """
    Описание структуры ответа обновления задания (полностью наследуется от GetExerciseResponseDict).
    """
    pass