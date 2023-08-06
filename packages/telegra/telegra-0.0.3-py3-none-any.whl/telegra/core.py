from cloudscraper import create_scraper
from .utils import *
from . import utils
import requests
import json


class Telegraph:
    """
    Description: interface to telegraph api
    Usage: `Telegraph(mirror="https://tg.foxe6.cf")`

    :param title: title
    :param author: author
    :param author_url: author url
    :param mirror: telegraph mirror url (server needs to proxy request)
    """
    def __init__(
            self,
            *,
            title="test", # type: str
            author="foxe6", # type: str
            author_url="https://tg.foxe6.cf", # type: str
            mirror="https://tg.foxe6.cf" # type: str
    ) -> None:
        # Description: telegraph title
        # Usage: `[instance].title`
        self.title = title # type: str
        # Description: telegraph author
        # Usage: `[instance].author`
        self.author = author # type: str
        # Description: telegraph author url
        # Usage: `[instance].author_url`
        self.author_url = author_url # type: str
        # Description: pixiv mirror url (server requires account to proxy request)
        # Usage: `[instance].mirror`
        self.mirror = mirror # type: str
        # Description: telegraph content
        # Usage: `[instance].content`
        self.content = [] # type: list
        # Description: requests.Session
        # Usage: `[instance].s`
        self.s = create_scraper() # type: requests.Session

    def save(
            self,
            Data, # type: str
            title, # type: str
            author, # type: str
            author_url, # type: str
            save_hash, # type: str
            page_id # type: str
    ) -> dict:
        """
        Description: internal raw request
        Usage: `[instance].save(...)`

        :param Data: ...
        :param title: ...
        :param author: ...
        :param author_url: ...
        :param save_hash: ...
        :param page_id: ...
        :return: json
        """
        r= self.s.post(self.mirror+"/save", files={
            "Data": ("content.html", Data, "plain/text"),
            "title": (None, title),
            "author": (None, author),
            "author_url": (None, author_url),
            "save_hash": (None, save_hash),
            "page_id": (None, page_id),
        })
        r=r.json()
        return r

    def publish(
            self
    ) -> json:
        """
        Description: publish this telegraph
        Usage: `[instance].publish()`

        :return: json
        """
        def loop(e):
            if isinstance(e, list):
                return list(map(loop, e))
            elif isinstance(e, dict):
                return {k: loop(v) for k, v in e.items()}
            elif isinstance(e, TGE):
                return loop(e.obj)
            else:
                return e
        data = self.content
        data = json.dumps(loop(data))
        return self.save(
            Data=data,
            title=self.title,
            author=self.author,
            author_url=self.author_url,
            save_hash="",
            page_id=0,
        )

    def A(
            self,
            *args,
            **kwargs
    ) -> utils.A:
        """
        Description: shortcut to `utils.A`
        Usage: `[instance].A(\\n    href="http://...",\\n    text="text"\\n)`

        :param args: will be passed to `utils.A`
        :param kwargs: will be passed to `utils.A`
        :return: utils.A
        """
        t = A(*args, **kwargs)
        return t

    def EM(
            self,
            *args,
            **kwargs
    ) -> utils.EM:
        """
        Description: shortcut to `utils.EM`
        Usage: `[instance].EM("text")`

        :param args: will be passed to `utils.EM`
        :param kwargs: will be passed to `utils.EM`
        :return: utils.EM
        """
        t = EM(*args, **kwargs)
        return t

    def STRONG(
            self,
            *args,
            **kwargs
    ) -> utils.STRONG:
        """
        Description: shortcut to `utils.STRONG`
        Usage: `[instance].STRONG("text")`

        :param args: will be passed to `utils.STRONG`
        :param kwargs: will be passed to `utils.STRONG`
        :return: utils.STRONG
        """
        t = STRONG(*args, **kwargs)
        return t

    def p(
            self,
            *args,
            **kwargs
    ) -> utils.P:
        """
        Description: shortcut to `utils.P`, will be appended to `[instance].content`
        Usage: `[instance].p("text")`

        :param args: will be passed to `utils.P`
        :param kwargs: will be passed to `utils.P`
        :return: utils.P
        """
        t = P(*args, **kwargs)
        self.content.append(t)
        return t

    def blockquote(
            self,
            *args,
            **kwargs
    ) -> utils.BLOCKQUOTE:
        """
        Description: shortcut to `utils.BLOCKQUOTE`, will be appended to `[instance].content`
        Usage: `[instance].blockquote("text")`

        :param args: will be passed to `utils.BLOCKQUOTE`
        :param kwargs: will be passed to `utils.BLOCKQUOTE`
        :return: utils.BLOCKQUOTE
        """
        t = BLOCKQUOTE(*args, **kwargs)
        self.content.append(t)
        return t

    def aside(
            self,
            *args,
            **kwargs
    ) -> utils.ASIDE:
        """
        Description: shortcut to `utils.ASIDE`, will be appended to `[instance].content`
        Usage: `[instance].aside("text")`

        :param args: will be passed to `utils.ASIDE`
        :param kwargs: will be passed to `utils.ASIDE`
        :return: utils.ASIDE
        """
        t = ASIDE(*args, **kwargs)
        self.content.append(t)
        return t

    def h3(
            self,
            *args,
            **kwargs
    ) -> utils.H3:
        """
        Description: shortcut to `utils.H3`, will be appended to `[instance].content`
        Usage: `[instance].h3("text")`

        :param args: will be passed to `utils.H3`
        :param kwargs: will be passed to `utils.H3`
        :return: utils.H3
        """
        t = H3(*args, **kwargs)
        self.content.append(t)
        return t

    def h4(
            self,
            *args,
            **kwargs
    ) -> utils.H4:
        """
        Description: shortcut to `utils.H4`, will be appended to `[instance].content`
        Usage: `[instance].h4("text")`

        :param args: will be passed to `utils.H4`
        :param kwargs: will be passed to `utils.H4`
        :return: utils.H4
        """
        t = H4(*args, **kwargs)
        self.content.append(t)
        return t

    def figure(
            self,
            *args,
            **kwargs
    ) -> utils.FIGURE:
        """
        Description: shortcut to `utils.FIGURE`, will be appended to `[instance].content`
        Usage: `[instance].figure(\\n    src="http://...",\\n    caption="text"\\n)`

        :param args: will be passed to `utils.FIGURE`
        :param kwargs: will be passed to `utils.FIGURE`
        :return: utils.FIGURE
        """
        t = FIGURE(*args, **kwargs)
        self.content.append(t)
        return t






