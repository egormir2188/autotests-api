from clients.courses.courses_client import get_course_client
from clients.exercises.exercises_client import get_exercises_client
from clients.files.files_cliet import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from tools.fakers import get_random_email

public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email = get_random_email(),
    password = 'string',
    last_name = 'string',
    first_name= 'string',
    middle_name = 'string'
)

create_user_response = public_users_client.create_user(create_user_request)

authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)

files_client = get_files_client(authentication_user)
courses_client = get_course_client(authentication_user)

create_file_request = CreateFileRequestSchema(
    filename = 'image.png',
    directory = 'courses',
    upload_file = './testdata/files/image.png'
)

create_file_response = files_client.create_file(create_file_request)
print('Create file data', create_file_response)

create_course_request = CreateCourseRequestSchema(
    title = 'Course',
    max_score = 10,
    min_score = 1,
    description = 'description',
    preview_file_id = create_file_response.file.id,
    estimated_time = '10 min',
    created_by_user_id = create_user_response.user.id
)

create_course_response = courses_client.create_course(create_course_request)
print('Create course data', create_course_response)

exercise_client = get_exercises_client(authentication_user)

create_exercise_request = CreateExerciseRequestSchema(
    title = 'Exercise',
    course_id = create_course_response.course.id,
    max_score = 10,
    min_score = 0,
    order_index = 0,
    description = "string",
    estimated_time = "2 days"
)

create_exercise_response = exercise_client.create_exercise(create_exercise_request)
print('Create exercise data:', create_exercise_response)