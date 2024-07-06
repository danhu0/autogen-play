import autogen

config_list = autogen.config_list_from_json(env_or_file="secrets/OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list}

tasks = [
    """On which days in 2024 was Microsoft Stock higher than $400? Comment on the stock performance.""",
    """Make a pleasant joke about it.""",
]

inner_assistant = autogen.AssistantAgent(
    "Inner-assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

inner_code_interpreter = autogen.UserProxyAgent(
    "Inner-code-interpreter",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    default_auto_reply="",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

groupchat = autogen.GroupChat(
    agents=[inner_assistant, inner_code_interpreter],
    messages=[],
    speaker_selection_method="round_robin",  # With two agents, this is equivalent to a 1:1 conversation.
    allow_repeat_speaker=False,
    max_round=8,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

