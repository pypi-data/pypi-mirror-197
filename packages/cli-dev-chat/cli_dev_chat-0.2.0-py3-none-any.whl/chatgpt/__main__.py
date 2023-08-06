import os
import openai
import argparse
from .snapshot import take_snapshot


def main():
    # Check if the OpenAI API key is already set as an environment variable
    if "OPENAI_API_KEY" in os.environ:
        openai.api_key = os.environ["OPENAI_API_KEY"]
    else:
        # Prompt the user to enter their API key
        api_key = input("Please enter your OpenAI API key: ")
        print(
            "Add the following line to your .bashrc file to avoid manually providing your api key in future:"
        )
        print(f"export OPENAI_API_KEY={api_key}")

        openai.api_key = api_key

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        "-m",
        default="gpt-3.5-turbo",
        help="The name of the GPT-3 model to use",
    )
    parser.add_argument(
        "paths", nargs="*", default=[], help="Filepaths or globlike strings"
    )
    parser.add_argument(
        "--filenames-only", "-fn", action="store_true", help="Print only the filenames"
    )
    parser.add_argument(
        "--content",
        "-c",
        action="store_true",
        help="Show the contents of each file shown to the AI assistant",
    )
    args = parser.parse_args()

    files, snapshot = take_snapshot(*args.paths, filenames_only=args.filenames_only)

    model = args.model
    messages = []

    def print_message(content, role=None, **kwargs):
        if role == "system":
            color = "\033[1;36m"  # cyan
            if args.content:
                pass
            elif files:
                content = (
                    f"You are working with a programming assistant powered by OpenAI on the following code:\n"
                    + "\n".join(files)
                )
            else:
                content = (
                    f"You are working with a programming assistant powered by OpenAI"
                )

        elif role == "user":
            color = "\033[1;32m"  # green
        elif role == "assistant":
            color = "\033[1;34m"  # blue
        else:
            color = "\033[0m"  # default
        print(color + content + "\033[0m", **kwargs)

    # Define a function to get user input and validate it
    def get_user_input():
        user_input = input("\033[1;32mYou: \033[0m")
        if len(user_input) == 0:
            print("Please enter something.")
            return get_user_input()
        elif len(user_input) > 256:
            print("Please enter something shorter.")
            return get_user_input()
        else:
            return user_input

    # Define a function to stream responses from OpenAI API using SSE
    def stream_response():
        stream = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.7,
            stream=True,
        )

        full_response = []
        try:
            for assistant_message in stream:
                choices = assistant_message.get("choices")
                if not choices:
                    continue
                delta = choices[0].get("delta")
                if not delta:
                    continue
                content = delta.get("content")
                if not content:
                    continue
                full_response.append(content)
                print_message(content, role="assistant", end="")
        except KeyboardInterrupt:
            stream.close()
            pass
        print()
        return "".join(full_response)

    # Start the chat session with a system message
    system_message = {
        "role": "system",
        "content": "You are working with a programming assistant powered by OpenAI on the following code:\n"
        + snapshot,
    }
    messages.append(system_message)
    print_message(system_message["content"], role=system_message["role"])

    # Loop until the user types "quit"
    while True:
        # Get user input and append it to messages list
        user_message = {"role": "user", "content": get_user_input()}

        if user_message["content"].lower() == "quit":
            break

        if user_message["content"].lower() == "show":
            print(messages)
            continue

        messages.append(user_message)

        # Stream response from OpenAI API using SSE
        messages.append({"role": "assistant", "content": stream_response()})


if __name__ == "__main__":
    main()
