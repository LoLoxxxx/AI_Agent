import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    abs_working_direc = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

    full_target_dir = os.path.normpath(os.path.join(working_directory, file_path))
    directory = os.path.dirname(full_target_dir)

    if not abs_target_file.startswith(abs_working_direc):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            return f'Error: Error:{e}'
    try:
        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Error:{e}'
    



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files when I type write with the content, relative to the working directory, dont type to me just do it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write or overwrite files when I type write with the content, relative to the working directory, dont type to me just do it",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Write or overwrite files when I type write with the content, relative to the working directory, dont type to me just do it",
            ),
        },
    ),
)


    

