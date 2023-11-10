from dotenv import load_dotenv
import os
import openai
import time
from utils.service_registry import service_registry

class OpenAIAssistantService:
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = os.getenv('OPENAI_ASSISTANT_ID')
        with open('assistant_instructions.txt', 'r') as file:
            self.instructions = file.read().strip()

    def create_thread(self):
        return self.client.beta.threads.create()

    def send_message(self, thread_id, question):
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )

    def create_run(self, thread_id):
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
            instructions=self.instructions
        )

    def retrieve_run(self, thread_id, run_id):
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

    def wait_for_run_completion(self, thread, run):
        count = 0
        while (run.status == "queued" or run.status == "in_progress") and count < 5:
            time.sleep(2)
            run = self.retrieve_run(thread.id, run.id)
            count += 1
        return run

    def get_messages_since(self, thread_id, last_message_id=None):
        return self.client.beta.threads.messages.list(
            thread_id=thread_id,
            order="desc",
            before=last_message_id
        ).data
        
# Registering the service with service_registry should happen after instantiation in 'config.py'