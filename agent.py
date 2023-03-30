from langchain.agents import initialize_agent

from chatgpt import RevChatGPT, OpenAIChatGPT
from tools import GoogleSearchTool

tools = [GoogleSearchTool()]

agent = initialize_agent(tools, RevChatGPT(), agent="zero-shot-react-description", verbose=True)

question = input("Input Your Question: ")
agent.run(question)
