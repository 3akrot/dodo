import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
import json

from call_function import available_functions, call_function
from prompts import system_prompt

loaded = load_dotenv()


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("api key is missing")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    user_propmt = args.user_prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_propmt},
    ]
    for _ in range(20):
        response = client.chat.completions.create(
            model="z-ai/glm-5.3-flash",
            messages=messages,
            tools=available_functions
        )
        if response.usage is not None and args.__getattribute__("verbose"):
            print(f"User prompt: {user_propmt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        elif response.usage is None:
            raise RuntimeError("failed to track usage")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_result = call_function(tool_call, args.__getattribute__("verbose"))
                if tool_result['content'] == "":
                    raise Exception("tool returned an empty string")
                    
                if args.verbose:
                    print(f"-> {tool_result['content']}")
                messages.append(tool_result)
        else:
            print(response.choices[0].message.content)
            break
        if _ == 19:
            print("too many iterations")
              
    


if __name__ == "__main__":
    main()
