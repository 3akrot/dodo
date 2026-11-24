import os
import subprocess

from functions.util import is_within_dir

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "run a python file in a specified directory relative to the working directory, providing file content",
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
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        wd_absloute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(wd_absloute_path, file_path))
    
        if is_within_dir(working_directory, file_path) == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if os.path.exists(target_path) and os.path.isfile(target_path):
            if target_path.endswith(".py") == False:
                return f'Error: "{file_path}" is not a Python file'
            command = ["python", target_path]
            if args:
                command.extend(args)
            procces = subprocess.run(
                command,
                cwd=os.path.abspath(working_directory),
                text=True,
                timeout=30,
                stdout=True,
                stderr=True,
            )
            if procces.returncode != 0:
                return f"Process exited with code {procces.returncode}"
            if procces.stdout == "" and procces.stderr == "":
                return "No output produced"
            output = ""
            output += f"STDOUT: {procces.stdout}"
            output += f"STDERR: {procces.stderr}"
            return output
        else:
            return f'Error: "{file_path}" does not exist or is not a regular file'
    except Exception as e:
        return f"Error: executing Python file: {e}"
