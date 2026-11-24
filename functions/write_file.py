import os

from functions.util import is_within_dir
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "write a file in a specified directory relative to the working directory, providing file content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to a file, relative to the working directory",
                },
                "content":{
                    "type": "string",
                    "description": "the content of the file to write"
                }
            },
        },
    },
}
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        wd_absloute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(wd_absloute_path, file_path))
        
        if is_within_dir(working_directory, file_path) == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        if os.path.exists(target_path):
            os.remove(target_path)
        with open(target_path, mode="x") as file:
            length = file.write(content)
            return f'Successfully wrote to "{file_path}" ({length} characters written)'
    except Exception as e:
        return f"Error {e.args[1]} while writing to {file_path}"
    