from wxauto import WeChat
from autogen_wx_utils import AIChatManager

import os
import time
from dotenv import load_dotenv
import sys

wx = WeChat()
listen_list = [
    'Weiping'
]

def get_last_message(wx, listen_list):
    new_message = None
    # Retrieve all messages
    msgs = wx.GetAllMessage()
    msg_list = []
    for chat in msgs:
        if chat[0] in listen_list:
            msg_list.append(chat)
    return msg_list[-1]

chat_manager = AIChatManager(config_path="secrets/OAI_CONFIG_LIST.json")
# chat_manager.initiate_chat("Hello")

old_msg = None
while True:
    new_msg = get_last_message(wx, listen_list)
    time.sleep(1)
    if str(old_msg) != str(new_msg):
        # print(new_msg)
        old_msg = new_msg
        chat_manager.send_feedback(str(new_msg))
        print(chat_manager.get_last_response())
        wx.SendMsg(chat_manager.get_last_response().get('content'), listen_list[0])
        

        