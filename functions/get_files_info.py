import os

from functions.util import is_within_dir

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir = os.path.normpath(os.path.join(working_directory, directory)) 
        if os.path.isfile(directory):
            return f'Error: "{directory}" is not a directory'

        if is_within_dir(working_directory, directory) == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        dir_content:list[str] = []
        for entry_name in os.listdir(target_dir):
            entry_path = os.path.join(target_dir,entry_name)
            dir_content.append(f"- {entry_name}: file_size={os.path.getsize(entry_path)} bytes, is_dir={os.path.isdir(entry_path)}")
        return "\n".join(dir_content)
        

    except Exception as e:
        return f"Error: {e.__cause__}"
