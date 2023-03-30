import os
from typing import Any, List, Mapping, Optional

import streamlit as st
from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain.llms.base import LLM
from langchain.tools import BaseTool
from pydantic import BaseModel

from chatgpt import ask_chatgpt, ask_chatgpt_with_stop
from tools import google_search
from utils import ConfigReader

os.environ["OPENAI_API_KEY"] = ConfigReader().get("openai", "key")
openai_llm = OpenAI(temperature=0)


class CustomLLM(LLM, BaseModel):
    llm_name = "custom_llm"

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        prompt = prompt.replace(
            "Begin!",
            "Please answer in Chinese in the follow-up sessions!"
        )
        # thought = ask_chatgpt_with_stop(prompt=prompt, stop=stop)
        thought = openai_llm.__call__(prompt=prompt, stop=stop).strip()
        st.text_area(label="Thought", value=thought)
        return thought

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}


class GoogleSearchTool(BaseTool):
    name = "Google-Search"
    description = "useful for when you need to answer questions about current events"

    def _run(self, query: str) -> str:
        """Use the tool."""
        google_res = google_search(query)
        items = google_res["items"]
        titles, snippets = [], []
        try:
            contexts = []
            for idx, item in enumerate(items[:5]):
                titles.append(item['title'])
                snippets.append(item['snippet'])
                contexts.append('[{}]: {} [{}]'.format(idx, item['snippet'], item['link']))
            st.text_area(label="Observation", value='\n'.join(contexts), height=200)
            contents = ['{}'.format(snippet) for title, snippet in zip(titles, snippets)]
            return '\n'.join(contents)
        except Exception:
            return ''

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError()


tools = [GoogleSearchTool()]

agent = initialize_agent(tools, CustomLLM(), agent="zero-shot-react-description", verbose=True)

question = st.text_input("Question")

if len(question):
    answer = agent.run(question)
    st.text_area(label="Answer", value=answer)
