import json
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from weather import get_weather

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
functions = {
    "get_weather": get_weather
}

with open('assistant_instructions.txt', 'r') as file:
    instructions = file.read().strip()


def create_thread():
    return client.beta.threads.create()


def send_message(thread, question):
    return client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )


def create_run(thread):
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions=instructions
    )


def retrieve_run(thread, run):
    return client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )


def wait_for_run_completion(thread, run):
    count = 0
    while (run.status == "queued" or run.status == "in_progress") and count < 5:
        time.sleep(2)
        run = retrieve_run(thread, run)
        count += 1
    return run


def execute_required_functions(required_actions):
    tool_outputs = []
    for tool_call in required_actions.submit_tool_outputs.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        if func_name in functions:
            function = functions[func_name]
            result = function(**args)

            result_str = json.dumps(result)

            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": result_str,
            })

    return tool_outputs


def assist():
    thread = create_thread()
    last_message_id = None

    while True:
        question = input("user: ")

        if question.lower() == "exit":
            print("Exiting the chat.")
            break

        try:
            message = send_message(thread, question)
            last_message_id = message.id

            run = create_run(thread)
            run = retrieve_run(thread, run)

            run = wait_for_run_completion(thread, run)

            if run.status == "requires_action":
                tool_outputs = execute_required_functions(run.required_action)

                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            run = wait_for_run_completion(thread, run)

            thread_messages = client.beta.threads.messages.list(
                thread_id=thread.id,
                order="desc",
                before=last_message_id
            )

            for message in thread_messages.data:
                if message.role == "assistant":
                    message_text = message.content[0].text.value
                    print(f"\nassistant: {message_text}\n")
                    last_message_id = message.id

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    assist()