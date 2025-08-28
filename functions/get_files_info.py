import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = ""
    path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(path)
        lines = []
        for item in contents:
            full_path = os.path.join(path, item)
            size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            line = f'- {item}: file_size={size} bytes, is_dir={is_dir}'
            lines.append(line)

        result = '\n'.join(lines)
        return result
    except Exception as e:
        return f"Error:{e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    


