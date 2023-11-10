import json
from utils.service_registry import service_registry

class InteractionHandler:
    def __init__(self):
        self.openai_assistant_service = service_registry.get_service('OpenAIAssistantService')

    def handle_user_input(self, user_input):
        thread = self.openai_assistant_service.create_thread()
        self.openai_assistant_service.send_message(thread.id, user_input)
        run = self.openai_assistant_service.create_run(thread.id)
        run = self.openai_assistant_service.wait_for_run_completion(thread, run)

        if run.status == "requires_action":
            tool_outputs = self.execute_required_functions(run.required_action)
            self.openai_assistant_service.client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            run = self.openai_assistant_service.wait_for_run_completion(thread, run)
        
        responses = self.openai_assistant_service.get_messages_since(thread.id)
        assistant_messages = [msg for msg in responses if msg.role == "assistant"]
        return assistant_messages[-1].content if assistant_messages else "No response from assistant."

    def execute_required_functions(self, required_actions):
        functions = service_registry.get_service('weather_service')  # As an example, we are using weather_service
        tool_outputs = []
        for tool_call in required_actions.submit_tool_outputs.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if func_name == "get_weather":
                result = functions.get_weather(**args)
                result_str = json.dumps(result)
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": result_str,
                })

        return tool_outputs