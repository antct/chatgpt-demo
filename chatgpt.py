import os
from typing import Any, List, Mapping, Optional

from langchain.llms import OpenAI
from langchain.llms.base import LLM
from pydantic import BaseModel

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


class RevChatGPT(LLM, BaseModel):
    llm_name = "RevChatGPT"

    @property
    def _llm_type(self) -> str:
        return RevChatGPT.llm_name

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        prompt = prompt.replace(
            "Begin!",
            "Please answer in Chinese in the follow-up sessions!"
        )
        thought = ask_chatgpt_with_stop(prompt=prompt, stop=stop)
        return thought

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}


os.environ["OPENAI_API_KEY"] = ConfigReader().get("openai", "key")
openai_llm = OpenAI(temperature=0)


class OpenAIChatGPT(LLM, BaseModel):
    llm_name = "OpenAIChatGPT"

    @property
    def _llm_type(self) -> str:
        return OpenAIChatGPT.llm_name

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        prompt = prompt.replace(
            "Begin!",
            "Please answer in Chinese in the follow-up sessions!"
        )
        return openai_llm.__call__(prompt=prompt, stop=stop)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}


if __name__ == "__main__":
    print(ask_chatgpt("你好呀！"))
