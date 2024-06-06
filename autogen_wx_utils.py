import autogen

class AIChatManager:
    def __init__(self, config_path, work_dir="coding", use_docker=False):
        self.config_list = autogen.config_list_from_json(env_or_file=config_path)
        self.assistant = autogen.AssistantAgent(
            name="Assistant",
            llm_config={
                "config_list": self.config_list
            }
        )
        # self.assistant.register_reply()

        self.user_proxy = autogen.UserProxyAgent(
            name="user",
            human_input_mode="ALWAYS",
            code_execution_config={
                "work_dir": work_dir,
                "use_docker": use_docker
            }
        )

    def initiate_chat(self, initial_message):
        self.user_proxy.initiate_chat(self.assistant, message=initial_message)

    def send_feedback(self, feedback_message):
        self.user_proxy.send(feedback_message, self.assistant, request_reply=True, silent=False)

    def get_last_response(self):
        messages = self.user_proxy.chat_messages[self.assistant] 
        last_message = messages[-1]
        return last_message