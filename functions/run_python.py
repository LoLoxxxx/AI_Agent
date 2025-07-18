import os
import subprocess
from dotenv import load_dotenv
from google import genai
from google.genai import types
def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    abs_working_direc = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_target_file.startswith(abs_working_direc):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target_file):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commmand = ['python3', file_path] + args
        output = []
        process = subprocess.run(commmand, cwd=working_directory, timeout=30, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    

        if process.stdout:
            output.append("STDOUT:\n" + process.stdout.strip())
        if process.stderr:
            output.append("STDERR:\n" + process.stderr.strip())
        if process.returncode != 0:
            output.append(f'Process exited with code {process.returncode}')
        if not output:
            return 'No output produced.'
        
        joined_output = " ".join(output)
        return joined_output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, relative to the working directory, you dont need any argumenst, dont type to me just do it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="Execute Python files with optional arguments, relative to the working directory, dont type to me just do it",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Execute Python files with optional arguments, relative to the working directory, dont type to me just do it",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Execute Python files with optional arguments, relative to the working directory, dont type to me just do it",
            ),
        },
    ),
)
    

  

