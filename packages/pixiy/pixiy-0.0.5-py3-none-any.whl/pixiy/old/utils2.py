import pixivpy3
import os
import re


dir0 = os.path.dirname(os.path.abspath(__file__))
dir = os.path.dirname(os.path.abspath(pixivpy3.__file__))
core = '''\
from cloudscraper import create_scraper
from typing import Any, Dict, Optional
import requests

try:
    # Python>=3.8
    from typing import Literal  # type: ignore[attr-defined]
except ImportError:
    # Python==3.6, ==3.7
    from typing_extensions import Literal

try:
    # Python>=3.10
    from typing import TypeAlias  # type: ignore[attr-defined]
except ImportError:
    # Python==3.6, ==3.7, ==3.8, ==3.9
    from typing_extensions import TypeAlias

from requests.structures import CaseInsensitiveDict

ParamDict = Optional[Dict[str, Any]]
ParsedJson = Any
Response = Any


# @typechecked
class PixivError(Exception):
    ...

# from typeguard import typechecked


_FILTER: TypeAlias = Literal["for_ios", ""]
_TYPE: TypeAlias = Literal["illust", "manga", ""]
_RESTRICT: TypeAlias = Literal["public", "private", ""]
_CONTENT_TYPE: TypeAlias = Literal["illust", "manga", ""]
_MODE: TypeAlias = Literal[
    "day",
    "week",
    "month",
    "day_male",
    "day_female",
    "week_original",
    "week_rookie",
    "day_manga",
    "day_r18",
    "day_male_r18",
    "day_female_r18",
    "week_r18",
    "week_r18g",
    "",
]
_SEARCH_TARGET: TypeAlias = Literal[
    "partial_match_for_tags", "exact_match_for_tags", "title_and_caption", "keyword", ""
]
_SORT: TypeAlias = Literal["date_desc", "date_asc", "popular_desc", ""]
_DURATION: TypeAlias = Literal[
    "within_last_day", "within_last_week", "within_last_month", "", None
]
_BOOL: TypeAlias = Literal["true", "false"]

class Pixiy:
    @staticmethod
    def download(url):
        url = url.split("/", 2)
        return requests.get("https://i.pximg.net"+url[2], headers={
            "referer": "https://www.pixiv.net/"
        })
        
    def post(self, data):
        r = create_scraper().post(self.mirror+"/api?"+data.pop("op")+("&"+self.token if self.token else ""), data=data)
        try:
            return r.json()
        except:
            return r.content.decode()

    def __init__(self, mirror = "https://pixiv.foxe6.cf", token = "") -> None:
        self.mirror = mirror
        self.token = token
'''
for fn in os.listdir(dir):
    fp = os.path.join(dir, fn)
    c = open(fp, "rb").read().decode()
    if "class AppPixivAPI" in c:
        print(fp)
        c = c.splitlines()
        i = 0
        for i, l in enumerate(c):
            if "class AppPixivAPI" in l:
                break
        print(i)
        while True:
            if i >= len(c)-1:
                break
            if " def " in c[i]:
                func = ""
                # print(c[i])
                func += " "*4+c[i].strip()
                if ")" not in c[i]:
                    i+=1
                    while True:
                        if i >= len(c)-1:
                            break
                        # print(c[i])
                        func += "\n"+" "*8+c[i].strip()
                        if ")" in c[i]:
                            break
                        i+=1
                func = func.replace(" "*8+")", " "*4+")")
                func2 = "".join(_.strip() for _ in func.splitlines())
                __ = func2.split("(")
                defn = __[0].split("def")[1].strip()
                args = __[1].split(")")[0].split(",")
                args.pop(0)
                args = [_.split(":")[0].strip() for _ in args if _]
                print(args)
                func += "\n"+" "*8+"return self.post(dict({}, {}))\n".format("{}=\"{}\"".format(
                    "op",
                    defn
                ), ", ".join("{}={}".format(_, _) for _ in args))
                core += "\n"+func
            i+=1
        break
core = re.sub(r"([A-Z_a-z]+): [a-z\|A-Z\-. _\[\]]+( = )", r"\g<1>\g<2>", core)
core = re.sub(r"([A-Z_a-z]+): [a-z\|A-Z\-. _\[\]]+", r"\g<1>", core)
core = re.sub(r"dict\[", r"Dict[", core)
core = re.sub(r"-> [A-Z\[\]a-z, ]+ \| [A-Z\[\]a-z, ]+", r"-> None", core)
open(os.path.join(dir0, "utils.py"), "wb").write(core.encode())
