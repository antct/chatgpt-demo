import random

from googleapiclient.discovery import build
from langchain.tools import BaseTool

from utils import ConfigReader, retry


@retry(times=2)
def google_search(query):
    config = ConfigReader()
    keys = eval(config.get("google", "keys"))
    cxs = eval(config.get("google", "cxs"))

    assert len(keys) == len(cxs)

    idx = random.randint(0, len(keys) - 1)
    key = keys[idx]
    cx = cxs[idx]

    service = build(
        "customsearch", "v1", developerKey=key
    )
    res = (
        service.cse()
        .list(
            q=query,
            cx=cx,
        )
        .execute()
    )
    return res


class GoogleSearchTool(BaseTool):
    name = "Google-Search"
    description = "useful for when you need to answer questions about current events"

    def _run(self, query: str) -> str:
        """Use the tool."""
        google_res = google_search(query)
        items = google_res["items"]
        titles, snippets = [], []
        try:
            for idx, item in enumerate(items[:5]):
                titles.append(item['title'])
                snippets.append(item['snippet'])
            contents = ['{}'.format(snippet) for title, snippet in zip(titles, snippets)]
            return '\n'.join(contents)
        except Exception:
            return ''

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError()


if __name__ == "__main__":
    print(google_search("浙江大学"))
