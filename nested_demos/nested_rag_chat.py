from typing_extensions import Annotated

import autogen
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

config_list = autogen.config_list_from_json(env_or_file="secrets/OAI_CONFIG_LIST.json")
llm_config = {
    "cache_seed": 43,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,  # in seconds
}

task = """Write a concise but engaging blogpost about Autogen."""

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",
        "docs_path": "https://raw.githubusercontent.com/microsoft/autogen/main/README.md",
    },
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    }
)

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config={"config_list": config_list},
    system_message="""
    You are a professional writer, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.
    You should imporve the quality of the content based on the feedback from the user.
    """,
)

# user_proxy = autogen.UserProxyAgent(
#     name="User",
#     human_input_mode="NEVER",
#     is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
#     code_execution_config={
#         "last_n_messages": 1,
#         "work_dir": "tasks",
#         "use_docker": False,
#     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
# )

critic = autogen.AssistantAgent(
    name="Critic",
    llm_config={"config_list": config_list},
    system_message="""
    You are a critic, known for your thoroughness and commitment to standards.
    Your task is to scrutinize content for any harmful elements or regulatory violations, ensuring
    all materials align with required guidelines.
    For code
    """,
)

def reflection_message(recipient, messages, sender, config):
    print("Reflecting...", "yellow")
    return f"Reflect and provide critique on the following writing. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"


ragproxyagent.register_nested_chats(
    [{"recipient": critic, "message": reflection_message, "summary_method": "last_msg", "max_turns": 1}],
    trigger=writer,  # condition=my_condition,
)

ragproxyagent.initiate_chat(recipient=writer, message=ragproxyagent.message_generator, problem="What is autogen?")

# res = user_proxy.initiate_chat(recipient=writer, message=task, max_turns=2, summary_method="last_msg")
# ragproxyagent.initiate_chat(assistant, message=ragproxyagent.message_generator, problem="What is autogen?")