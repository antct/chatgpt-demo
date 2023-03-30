from utils import ConfigReader


def ask_chatgpt(prompt):
    from revChatGPT.V1 import Chatbot

    # https://chat.openai.com/api/auth/session
    access_token = ConfigReader().get("chatgpt", "access_token")
    chatbot = Chatbot(config={
        "access_token": access_token
    })
    for data in chatbot.ask(prompt):
        message = data["message"]
    return message


def ask_chatgpt_with_stop(prompt, stop):
    from revChatGPT.V1 import Chatbot
    access_token = ConfigReader().get("chatgpt", "access_token")
    chatbot = Chatbot(config={
        "access_token": access_token
    })
    flag = False
    n = -1
    for data in chatbot.ask(prompt):
        message = data["message"]
        if flag:
            continue
        for s in stop:
            if s in message:
                flag = True
                n = message.rfind(s)
                break
    return message[:n]


if __name__ == "__main__":
    print(ask_chatgpt("你好呀！"))