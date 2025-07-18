import os
from google import genai
from google.genai import types


from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

DEFAULT_WORKING_DIRECTORY = './calculator'

def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    func_name = function_call_part.name
    func_args = dict(function_call_part.args)
    func_args["working_directory"] = DEFAULT_WORKING_DIRECTORY 

    if verbose == True:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f" - Calling function: {func_name}")

    if func_name not in function_map:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=func_name,
            response={"error": f"Unknown function: {func_name}"},
        )
    ],
)
    else:
        function_to_call = function_map[func_name]
        function_res = function_to_call(**func_args)
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_res},
            )
        ],
    )
    