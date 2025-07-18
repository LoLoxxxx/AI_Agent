import os
from google import genai
from google.genai import types
def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_direc = os.path.abspath(working_directory)

    if not abs_target_file.startswith(abs_working_direc):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    truncate_message = ''

    try:
        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                truncate_message = f'[...File \"{file_path}\" truncated at {MAX_CHARS} characters]'
        return file_content_string + truncate_message
    except Exception as e:
        return f'Error: {e}'
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents when I type read, constrained to the working directory, dont type to me just do it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Read file contents when I type read, constrained to the working directory, dont type to me just do it.",
            ),
        },
    ),
)
    