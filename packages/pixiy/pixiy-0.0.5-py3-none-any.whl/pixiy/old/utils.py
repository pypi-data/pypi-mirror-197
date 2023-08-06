from cloudscraper import create_scraper
from typing import Any, Dict, Optional

try:
    # Python>=3.8
    from typing import Literal  # type
except ImportError:
    # Python==3.6, ==3.7
    from typing_extensions import Literal

try:
    # Python>=3.10
    from typing import TypeAlias  # type
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


_FILTER = Literal["for_ios", ""]
_TYPE = Literal["illust", "manga", ""]
_RESTRICT = Literal["public", "private", ""]
_CONTENT_TYPE = Literal["illust", "manga", ""]
_MODE = Literal[
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
_SEARCH_TARGET = Literal[
    "partial_match_for_tags", "exact_match_for_tags", "title_and_caption", "keyword", ""
]
_SORT = Literal["date_desc", "date_asc", "popular_desc", ""]
_DURATION = Literal[
    "within_last_day", "within_last_week", "within_last_month", "", None
]
_BOOL = Literal["true", "false"]

class Pixiy:
    def post(self, data):
        r = create_scraper().post(self.mirror+"/api?"+data.pop("op")+("&"+token if token else ""), data=data)
        try:
            return r.json()
        except:
            return r.content.decode()

    def __init__(self, mirror = "https://pixiv.foxe6.cf", token = "") -> None:
        self.mirror = mirror
        self.token = token

    # def __init__(self, **requests_kwargs) -> None:
    #     return self.post(dict(op="__init__", **requests_kwargs=**requests_kwargs))
    #
    # def set_api_proxy(self, proxy_hosts = "http://app-api.pixivlite.com") -> None:
    #     return self.post(dict(op="set_api_proxy", proxy_hosts=proxy_hosts))
    #
    # def no_auth_requests_call(
    #     self,
    #     method,
    #     url,
    #     headers = None,
    #     params = None,
    #     data = None,
    #     req_auth = True,
    # ) -> Response:
    #     return self.post(dict(op="no_auth_requests_call", method=method, url=url, headers=headers, params=params, data=data, req_auth=req_auth))
    #
    # def parse_result(self, res) -> ParsedJson:
    #     return self.post(dict(op="parse_result", res=res))
    #
    # def format_bool(cls, bool_value) -> _BOOL:
    #     return self.post(dict(op="format_bool", bool_value=bool_value))
    #
    # def parse_qs(cls, next_url) -> None:
    #     return self.post(dict(op="parse_qs", next_url=next_url))

    def user_detail(
        self,
        user_id,
        filter = "for_ios",
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_detail", user_id=user_id, filter=filter, req_auth=req_auth))

    def user_illusts(
        self,
        user_id,
        type = "illust",
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_illusts", user_id=user_id, type=type, filter=filter, offset=offset, req_auth=req_auth))

    def user_bookmarks_illust(
        self,
        user_id,
        restrict = "public",
        filter = "for_ios",
        max_bookmark_id = None,
        tag = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_bookmarks_illust", user_id=user_id, restrict=restrict, filter=filter, max_bookmark_id=max_bookmark_id, tag=tag, req_auth=req_auth))

    def user_related(
        self,
        seed_user_id,
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_related", seed_user_id=seed_user_id, filter=filter, offset=offset, req_auth=req_auth))

    def illust_follow(
        self,
        restrict = "public",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_follow", restrict=restrict, offset=offset, req_auth=req_auth))

    def illust_detail(self, illust_id, req_auth = True) -> ParsedJson:
        return self.post(dict(op="illust_detail", illust_id=illust_id, req_auth=req_auth))

    def illust_comments(
        self,
        illust_id,
        offset = None,
        include_total_comments = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_comments", illust_id=illust_id, offset=offset, include_total_comments=include_total_comments, req_auth=req_auth))

    def illust_related(
        self,
        illust_id,
        filter = "for_ios",
        seed_illust_ids = None,
        offset = None,
        viewed = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_related", illust_id=illust_id, filter=filter, seed_illust_ids=seed_illust_ids, offset=offset, viewed=viewed, req_auth=req_auth))

    def illust_recommended(
        self,
        content_type = "illust",
        include_ranking_label = True,
        filter = "for_ios",
        max_bookmark_id_for_recommend = None,
        min_bookmark_id_for_recent_illust = None,
        offset = None,
        include_ranking_illusts = None,
        bookmark_illust_ids = None,
        include_privacy_policy = None,
        viewed = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_recommended", content_type=content_type, include_ranking_label=include_ranking_label, filter=filter, max_bookmark_id_for_recommend=max_bookmark_id_for_recommend, min_bookmark_id_for_recent_illust=min_bookmark_id_for_recent_illust, offset=offset, include_ranking_illusts=include_ranking_illusts, bookmark_illust_ids=bookmark_illust_ids, include_privacy_policy=include_privacy_policy, viewed=viewed, req_auth=req_auth))

    def novel_recommended(
        self,
        include_ranking_label = True,
        filter = "for_ios",
        offset = None,
        include_ranking_novels = None,
        already_recommended = None,
        max_bookmark_id_for_recommend = None,
        include_privacy_policy = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="novel_recommended", include_ranking_label=include_ranking_label, filter=filter, offset=offset, include_ranking_novels=include_ranking_novels, already_recommended=already_recommended, max_bookmark_id_for_recommend=max_bookmark_id_for_recommend, include_privacy_policy=include_privacy_policy, req_auth=req_auth))

    def illust_ranking(
        self,
        mode = "day",
        filter = "for_ios",
        date = None,
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_ranking", mode=mode, filter=filter, date=date, offset=offset, req_auth=req_auth))

    def trending_tags_illust(
        self, filter = "for_ios", req_auth = True
    ) -> ParsedJson:
        return self.post(dict(op="trending_tags_illust", filter=filter, req_auth=req_auth))

    def search_illust(
        self,
        word,
        search_target = "partial_match_for_tags",
        sort = "date_desc",
        duration = None,
        start_date = None,
        end_date = None,
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="search_illust", word=word, search_target=search_target, sort=sort, duration=duration, start_date=start_date, end_date=end_date, filter=filter, offset=offset, req_auth=req_auth))

    def search_novel(
        self,
        word,
        search_target = "partial_match_for_tags",
        sort = "date_desc",
        merge_plain_keyword_results = "true",
        include_translated_tag_results = "true",
        start_date = None,
        end_date = None,
        filter = None,
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="search_novel", word=word, search_target=search_target, sort=sort, merge_plain_keyword_results=merge_plain_keyword_results, include_translated_tag_results=include_translated_tag_results, start_date=start_date, end_date=end_date, filter=filter, offset=offset, req_auth=req_auth))

    def search_user(
        self,
        word,
        sort = "date_desc",
        duration = None,
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="search_user", word=word, sort=sort, duration=duration, filter=filter, offset=offset, req_auth=req_auth))

    def illust_bookmark_detail(
        self, illust_id, req_auth = True
    ) -> ParsedJson:
        return self.post(dict(op="illust_bookmark_detail", illust_id=illust_id, req_auth=req_auth))

    def illust_bookmark_add(
        self,
        illust_id,
        restrict = "public",
        tags = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_bookmark_add", illust_id=illust_id, restrict=restrict, tags=tags, req_auth=req_auth))

    def illust_bookmark_delete(
        self, illust_id, req_auth = True
    ) -> ParsedJson:
        return self.post(dict(op="illust_bookmark_delete", illust_id=illust_id, req_auth=req_auth))

    def user_follow_add(
        self,
        user_id,
        restrict = "public",
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_follow_add", user_id=user_id, restrict=restrict, req_auth=req_auth))

    def user_follow_delete(
        self, user_id, req_auth = True
    ) -> ParsedJson:
        return self.post(dict(op="user_follow_delete", user_id=user_id, req_auth=req_auth))

    def user_bookmark_tags_illust(
        self,
        restrict = "public",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_bookmark_tags_illust", restrict=restrict, offset=offset, req_auth=req_auth))

    def user_following(
        self,
        user_id,
        restrict = "public",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_following", user_id=user_id, restrict=restrict, offset=offset, req_auth=req_auth))

    def user_follower(
        self,
        user_id,
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_follower", user_id=user_id, filter=filter, offset=offset, req_auth=req_auth))

    def user_mypixiv(
        self,
        user_id,
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_mypixiv", user_id=user_id, offset=offset, req_auth=req_auth))

    def user_list(
        self,
        user_id,
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_list", user_id=user_id, filter=filter, offset=offset, req_auth=req_auth))

    def ugoira_metadata(
        self, illust_id, req_auth = True
    ) -> ParsedJson:
        return self.post(dict(op="ugoira_metadata", illust_id=illust_id, req_auth=req_auth))

    def user_novels(
        self,
        user_id,
        filter = "for_ios",
        offset = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="user_novels", user_id=user_id, filter=filter, offset=offset, req_auth=req_auth))

    def novel_series(
        self,
        series_id,
        filter = "for_ios",
        last_order = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="novel_series", series_id=series_id, filter=filter, last_order=last_order, req_auth=req_auth))

    def novel_detail(self, novel_id, req_auth = True) -> ParsedJson:
        return self.post(dict(op="novel_detail", novel_id=novel_id, req_auth=req_auth))

    def novel_text(self, novel_id, req_auth = True) -> ParsedJson:
        return self.post(dict(op="novel_text", novel_id=novel_id, req_auth=req_auth))

    def illust_new(
        self,
        content_type = "illust",
        filter = "for_ios",
        max_illust_id = None,
        req_auth = True,
    ) -> ParsedJson:
        return self.post(dict(op="illust_new", content_type=content_type, filter=filter, max_illust_id=max_illust_id, req_auth=req_auth))

    def showcase_article(self, showcase_id) -> ParsedJson:
        return self.post(dict(op="showcase_article", showcase_id=showcase_id))
