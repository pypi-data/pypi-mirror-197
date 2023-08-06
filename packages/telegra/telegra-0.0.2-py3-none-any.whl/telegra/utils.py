class TGE:
    pass

class STRONG(TGE):
    def __init__(self, text):
        self.tag = "strong"
        self.children = [text]

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "children": self.children,
        }

class EM(TGE):
    def __init__(self, text):
        self.tag = "em"
        self.children = [text]

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "children": self.children,
        }

class A(TGE):
    def __init__(self, href, text):
        self.tag = "a"
        self.attrs = {"href": href, "target": "_blank"}
        self.children = [text]

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": self.children,
        }


class P(TGE):
    def __init__(self, text):
        self.tag = "p"
        self.attrs = {"dirs": "auto"}
        self.children = [text]

    def append(self, A_or_str=""):
        self.children.append(A_or_str)

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": self.children,
        }


class ASIDE(TGE):
    def __init__(self, text):
        self.tag = "aside"
        self.attrs = {"dir": "auto"}
        self.children = [text]

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": self.children,
        }


class BLOCKQUOTE(TGE):
    def __init__(self, text):
        self.tag = "blockquote"
        self.attrs = {"dir": "auto"}
        self.children = [text]

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": self.children,
        }


class H3(TGE):
    def __init__(self, text):
        self.tag = "h3"
        self.attrs = {"dir": "auto", "id": "h3"}
        self.children = [text]

    def append(self, A_or_str=""):
        self.children.append(A_or_str)

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": self.children,
        }


class H4(TGE):
    def __init__(self, text):
        self.tag = "h4"
        self.attrs = {"dir": "auto", "id": "h4"}
        self.children = [text]

    def append(self, A_or_str=""):
        self.children.append(A_or_str)

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "children": self.children,
        }


class FIGURE(TGE):
    def __init__(self, src, caption=""):
        self.tag = "figure"
        self.children = [{
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
        }]

    @property
    def obj(self):
        return {
            "tag": self.tag,
            "children": self.children,
        }

