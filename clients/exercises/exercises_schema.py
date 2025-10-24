from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ShortExerciseSchema(BaseModel):
    """
    Короткое описание сущности Exerxise.
    """
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    title: str
    max_score: int
    min_score: int
    order_index: int
    description: str
    estimated_time: str

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

    course_id: str


class CreateExerciseResponseSchema(GetExerciseResponseSchema):
    """
    Описание структуры ответа создания задания (полностью наследуется от GetExerciseResponseDict).
    """
    pass

class UpdateExerciseRequestSchema(ShortExerciseSchema):
    """
    Описание структуры запроса для обновления задания.
    """
    pass

class UpdateExerciseResponseSchema(GetExerciseResponseSchema):
    """
    Описание структуры ответа обновления задания (полностью наследуется от GetExerciseResponseDict).
    """
    pass