class TGE:
    pass


class STRONG(TGE):
    """
    Description: &lt;b&gt;&lt;/b&gt; node
    Usage: `STRONG("text")` or `STRONG(EM("text"))`

    :param text: text or node
    """
    def __init__(
            self,
            text # type: str
    ):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "strong",
            "children": [text],
        }


class EM(TGE):
    """
    Description: &lt;em&gt;&lt;/em&gt; node
    Usage: `EM("text")` or `EM(STRONG("text"))`

    :param text: text or node
    """
    def __init__(
            self,
            text # type: str
    ):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "em",
            "children": [text],
        }


class A(TGE):
    """
    Description: &lt;a href="http://..." target="_blank"&gt;&lt;/a&gt; node
    Usage: `A(href="http://...", text="text")` or `EM(A(href="http://...", text="text"))`

    :param href: url
    :param text: text or node
    """
    def __init__(
            self,
            href, # type: str
            text # type: str
    ):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "a",
            "attrs": {"href": href, "target": "_blank"},
            "children": [text],
        }


class P(TGE):
    """
    Description: &lt;p&gt;&lt;/p&gt; node
    Usage: `P("text")`

    :param text: text or node
    """
    def __init__(
            self, 
            text # type: str
    ):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "p",
            "attrs": {"dirs": "auto"},
            "children": [text],
        }

    def append(
            self,
            child # type: str
    ) -> None:
        """
        Description: append child to `P`
        Usage: `[instance].append("text")` or `[instance].append(EM("text"))`

        :param child: text or node
        :return: None
        """
        self.obj["children"].append(child)


class ASIDE(TGE):
    """
    Description: &lt;aside&gt;&lt;/aside&gt; node
    Usage: `ASIDE("text")`

    :param text: text or node
    """
    def __init__(self, text):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "aside",
            "attrs": {"dirs": "auto"},
            "children": [text],
        }


class BLOCKQUOTE(TGE):
    """
    Description: &lt;blockquote&gt;&lt;/blockquote&gt; node
    Usage: `BLOCKQUOTE("text")`

    :param text: text or node
    """
    def __init__(self, text):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "blockquote",
            "attrs": {"dirs": "auto"},
            "children": [text],
        }


class H3(TGE):
    """
    Description: &lt;h3&gt;&lt;/h3&gt; node
    Usage: `H3("text")`

    :param text: text or node
    """
    def __init__(self, text):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "h3",
            "attrs": {"dirs": "auto", "id": "h3"},
            "children": [text],
        }

    def append(
            self,
            child # type: str
    ) -> None:
        """
        Description: append child to `H3`
        Usage: `[instance].append("text")` or `[instance].append(EM("text"))`

        :param child: text or node
        :return: None
        """
        self.obj["children"].append(child)


class H4(TGE):
    """
    Description: &lt;h4&gt;&lt;/h4&gt; node
    Usage: `H4("text")`

    :param text: text or node
    """
    def __init__(self, text):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "h4",
            "attrs": {"dirs": "auto", "id": "h4"},
            "children": [text],
        }

    def append(
            self,
            child # type: str
    ) -> None:
        """
        Description: append child to `H4`
        Usage: `[instance].append("text")` or `[instance].append(EM("text"))`

        :param child: text or node
        :return: None
        """
        self.obj["children"].append(child)


class FIGURE(TGE):
    """
    Description: &lt;figure&gt;&lt;/figure&gt; node
    Usage: `FIGURE("text")`

    :param text: text or node
    :param caption: text
    """
    def __init__(
            self,
            src, # type: str
            caption="" # type: str
    ):
        # Description: serialization
        # Usage: `[instance].obj`
        self.obj = { # type: dict
            "tag": "figure",
            "children": [{
                "tag": "div",
                "attrs": {"class": "figure_wrapper"},
                "children": [{
                    "tag": "img",
                    "attrs": {"src": src}
                }]
            }, {
                "tag": "figcaption",
                "attrs": {"dir": "auto"},
                "children": [caption]
            }],
        }

