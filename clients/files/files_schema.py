from pydantic import BaseModel, HttpUrl, Field, FilePath
from tools.fakers import fake


class FileSchema(BaseModel):
    """
    Описание структуры файла.
    """
    id: str
    filename: str = Field(default_factory=lambda: f'{fake.uuid4()}.png')
    directory: str
    url: HttpUrl

class CreateFileRequestSchema(BaseModel):
    """
    Описание структуры запроса для создания файла.
    """
    filename: str = Field(default_factory=lambda: f'{fake.uuid4()}.png')
    directory: str = Field(default='tests')
    upload_file: FilePath

class CreateFileResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание файла.
    """
    file: FileSchema

class GetFileResponseSchema(BaseModel):
    """
    Описание структуры запроса получения файла.
    """
    file: FileSchema