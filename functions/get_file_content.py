from config import MAX_FILE_CHARS
from functions.util import is_within_dir
import os
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read a file in a specified directory relative to the working directory, providing file content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to a file, relative to the working directory",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    target_path = os.path.normpath(os.path.join(working_directory, file_path))

    if is_within_dir(working_directory, file_path) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_path, encoding="utf-8") as file:
            content = file.read(MAX_FILE_CHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            return content
    except Exception as e:
        return f'Error: {e.args[1]} while reading {file_path}'
        