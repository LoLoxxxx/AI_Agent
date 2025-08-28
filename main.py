import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

from functions.call_function import call_function
from functions.call_function import available_functions
def main():
    load_dotenv()


    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = sys.argv[1:]


    if not args:
        print("TYPE THE QUESTION")
        sys.exit(1)

    verbose = False
    if '--verbose' in args:
        verbose = True
        args.remove('--verbose')

    user_prompt = ' '.join(args)
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error: {e}")
            return

        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
                function_responses = []
                for func_call in response.function_calls:
                    function_call_result = call_function(func_call, verbose)
                    if (
                        not function_call_result.parts
                        or not hasattr(function_call_result.parts[0], "function_response")
                        or not hasattr(function_call_result.parts[0].function_response, "response")
                    ):
                        raise RuntimeError("Function response not found!")

                    if verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                    function_responses.append(function_call_result.parts[0])

                
                user_message = types.Content(
                    role="user", parts=function_responses
                    )
                messages.append(user_message)
                continue
        if response.text:
            print()
            print(f"Final Response:")
            print()
            print(response.text)
            break

    

    
    

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f'User prompt: {user_prompt}')
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


    # print(f'{response.text}\n Prompt tokens: {response.usage_metadata.prompt_token_count}\n Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
