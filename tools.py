import random

from googleapiclient.discovery import build

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


if __name__ == "__main__":
    print(google_search("浙江大学"))
