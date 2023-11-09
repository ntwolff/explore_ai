import json
from openai import OpenAI
from weather import get_weather
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
functions = {
    "get_weather": get_weather
}

# Load the personality context once from assistant_instructions.txt
with open('assistant_instructions.txt', 'r') as file:
    instructions = file.read().strip()

# Function to interact with the chatbot
def assist():

    thread = client.beta.threads.create()
    last_message_id = None

    while True:
        question = input("user: ")
        if question.lower() == "exit":
            print("Exiting the chat.")
            break
        try:
            # Add user message to the thread
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )
            
            # Tag the message as seen
            last_message_id = message.id

            # Run assistant
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id,
                instructions=instructions
            )

            # Display assistant response
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            # Wait until it is not queued
            count = 0
            while(run.status == "queued" or run.status == "in_progress") and count < 5:
                time.sleep(2)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                count = count + 1

            if run.status == "requires_action":

                # Get the tool outputs by executing the required functions
                tool_outputs = execute_required_functions(run.required_action)

                # Submit the tool outputs back to the Assistant
                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            # Wait until it is not queued
            count = 0
            while(run.status == "queued" or run.status == "in_progress" or run.status == "requires_action") and count < 5:
                time.sleep(2)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                count = count + 1

            
            # Retrieve messages from thread after run complete            
            thread_messages = client.beta.threads.messages.list(
                thread_id=thread.id
                ,order="desc"
                ,before=last_message_id
            )
            #app.logger.debug(thread_messages.data)

            for message in thread_messages.data:
                if message.role == "assistant":
                    message_text = message.content[0].text.value
                    print(f"\nassistant: {message_text}\n")
                    last_message_id = message.id
            
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to call the assistant required functions and return their outputs as JSON strings
def execute_required_functions(required_actions):
    tool_outputs = []
    for tool_call in required_actions.submit_tool_outputs.tool_calls:
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        # Call the corresponding Python function
        if func_name in functions:
            function = functions[func_name]
            # Assuming all functions take a single dictionary argument
            result = function(**args)

            # Serialize the function's output to JSON
            result_str = json.dumps(result)

            # Add the result to the list of tool outputs
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": result_str,
            })

    return tool_outputs

if __name__ == "__main__":
    assist()