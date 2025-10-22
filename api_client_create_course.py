from clients.courses.courses_file import get_course_client, CreateCourseRequestDict
from clients.files.files_cliet import get_files_client, CreateFileRequestDict
from clients.private_http_builder import AuthenticationUserDict
from clients.users.public_users_client import get_public_users_client, CreateUsersRequestDict
from tools.fakers import get_random_email

public_users_client = get_public_users_client()

create_user_request = CreateUsersRequestDict(
    email = get_random_email(),
    password = 'string',
    lastName = 'string',
    firstName = 'string',
    middleName = 'string'
)

create_user_response = public_users_client.create_user(create_user_request)

authentication_user = AuthenticationUserDict(
    email=create_user_request["email"],
    password=create_user_request["password"]
)

files_client = get_files_client(authentication_user)
courses_client = get_course_client(authentication_user)

create_file_request = CreateFileRequestDict(
    filename = 'image.png',
    directory = 'courses',
    upload_file = './testdata/files/image.png'
)

create_file_response = files_client.create_file(create_file_request)
print('Create file response', create_file_response)

create_course_request = CreateCourseRequestDict(
    title = 'Course',
    maxScore = 10,
    minScore = 1,
    description = 'description',
    previewFileId = create_file_response['file']['id'],
    estimatedTime = '10 min',
    createdByUserId = create_user_response['user']['id']
)

create_course_response = courses_client.create_course(create_course_request)
print('Create course response', create_course_response)