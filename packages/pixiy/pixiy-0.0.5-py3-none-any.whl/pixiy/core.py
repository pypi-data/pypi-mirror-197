from cloudscraper import create_scraper
import requests


class Pixiy:
    """
    Description: interface to pixiv api
    Usage: `Pixiy(mirror="https://pixiv.foxe6.cf")`

    :param mirror: pixiv mirror url (server requires account to proxy request)
    """
    def __init__(
            self,
            *,
            mirror = "https://pixiv.foxe6.cf" # type: str
    ) -> None:
        # Description: pixiv mirror url (server requires account to proxy request)
        # Usage: `[instance].mirror`
        self.mirror = mirror # type: str

    def get(
            self,
            url, # type: str
            params=None, # type: dict
            headers=None # type: dict
    ) -> requests.Response:
        """
        Description: get url with given params
        Usage: `[instance].get(\\n    self.mirror+"/ajax/user/1234/illusts/bookmarks",\\n    params={\\n        "tag": "",\\n        "offset": "0",\\n        "limit": "48",\\n        "rest": "show"\\n    }\\n)`

        :param url: any str
        :param params: any dict
        :param headers: any dict
        :return: response
        """
        return create_scraper().get(url, params=params, timeout=10, headers=headers)

    def search_artworks(
            self,
            *,
            word, # type: str
            order="date_d", # type: str
            mode="all", # type: str
            p=1, # type: int
            s_mode="s_tag", # type: str
            type="all", # type: str
            scd=None, # type: str
            ecd=None # type: str
    ) -> dict:
        """
        Description: search artworks
        Usage: `[instance].search_artworks(\\n    word="3dcg",\\n    mode="r18",\\n    type="ugoira",\\n)`

        :param word: any str
        :param order: `"date_d"` or `"date"`
        :param mode: `"all"` or `"safe"` or `"r18"`
        :param p: page number, max: 1000
        :param s_mode: `"s_tag"` or `"s_tag_full"` or `"s_tc"`
        :param type: `"all"` or `"illust_and_ugoira"` or `"illust"` or `"ugoira"` or `"manga"`
        :param scd: start date, format: `yyyy-mm-dd`, max range: one year
        :param ecd: end date, format: `yyyy-mm-dd`, max range: one year
        :return: json
        """
        switch = "artworks"
        if type in [
            "illust_and_ugoira",
            "illust",
            "ugoira",
        ]:
            switch = "illustrations"
        elif type in [
            "manga",
        ]:
            switch = "manga"
        url = self.mirror+"/ajax/search/{}/{}".format(switch, word)
        params = {
            "word": word,
            "order": order,
            "mode": mode,
            "p": p,
            "s_mode": s_mode,
            "type": type,
        }
        if scd and ecd:
            params.update({
                "scd": scd,
                "ecd": ecd,
            })
        return self.get(url, params).json()

    def illust(
            self,
            *,
            illust_id # type: int
    ) -> dict:
        """
        Description: get info of illustration
        Usage: `[instance].illust(\\n    illust_id=1234,\\n)`

        :param illust_id: illustration id
        :return: json
        """
        url = self.mirror+"/ajax/illust/{}".format(illust_id)
        return self.get(url).json()

    def illust_pages(
            self,
            *,
            illust_id # type: int
    ) -> dict:
        """
        Description: get pages of illustration
        Usage: `[instance].illust_pages(\\n    illust_id=1234,\\n)`

        :param illust_id: illustration id
        :return: json
        """
        url = self.mirror+"/ajax/illust/{}/pages".format(illust_id)
        return self.get(url).json()

    def ugoira_meta(
            self,
            *,
            illust_id # type: int
    ) -> dict:
        """
        Description: get ugoria metadata of illustration
        Usage: `[instance].ugoira_meta(\\n    illust_id=1234,\\n)`

        :param illust_id: illustration id
        :return: json
        """
        url = self.mirror+"/ajax/illust/{}/ugoira_meta".format(illust_id)
        return self.get(url).json()

    def user_profile(
            self,
            *,
            user_id # type: int
    ) -> dict:
        """
        Description: get profile of user
        Usage: `[instance].user_profile(\\n    user_id=1234,\\n)`

        :param user_id: user id
        :return: json
        """
        url = self.mirror+"/ajax/user/{}/profile/all".format(user_id)
        return self.get(url).json()

    # def user_illusts(
    #         self,
    #         *,
    #         user_id, # type: int
    #         illusts # type: list
    # ) -> dict:
    #     """
    #     Description: get illustrations info of user from profile
    #     Usage: `[instance].user_illusts(\\n    user_id=1234,\\n    illusts=[1234,2345],\\n)`
    #
    #     :param user_id: user id
    #     :param illusts: list of illustration id
    #     :return: json
    #     """
    #     url = self.mirror+"/ajax/user/{}/illusts".format(user_id)
    #     params = "?"+"&".join("ids[]={}".format(_) for _ in illusts)
    #     return self.get(url+params).json()

    def illust_recommend(
            self,
            *,
            illust_id, # type: int
            limit=18 # type: int
    ) -> dict:
        """
        Description: get similar/related/recommended based on illust
        Usage: `[instance].illust_recommend(\\n    illust_id=1234,\\n    limit=18,\\n)`

        :param illust_id: illustration id
        :param limit: number
        :return: json
        """
        url = self.mirror+"/ajax/illust/{}/recommend/init".format(illust_id)
        params = {
            "limit": limit,
        }
        return self.get(url, params).json()

    def illusts(
            self,
            *,
            illusts # type: list
    ) -> dict:
        """
        Description: get info of illustrations
        Usage: `[instance].illusts(\\n    illusts=[1234,2345],\\n)`

        :param illust_id: illustration id
        :return: json
        """
        url = self.mirror+"/ajax/illust/recommend/illusts"
        params = "?"+"&".join("illust_ids[]={}".format(_) for _ in illusts)
        return self.get(url+params).json()

    def download(
            self,
            url # type: str
    ) -> bytes:
        """
        Description: download files from i.pximg.net
        Usage: `[instance].download(\\n    "https://i.pximg.net/c/..."\\n)`

        :param url: url
        :return: bytes
        """
        return create_scraper().get(self.mirror+"/"+url.replace("://", ":/")).content

