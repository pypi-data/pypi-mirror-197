from cloudscraper import create_scraper
import threadwrapper
import threading
from omnitools import def_template
from lxml import html
import time
import json
import os


sig = b'GIF89a\x01\x00\x01\x00p\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x81\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02D\x01\x00;'


class TgDrive:
    def __init__(
            self,
            *,
            mirror="https://telegra.ph" # type: str
    ) -> None:
        self.mirror = mirror

    def upload(self, fp, publish=True):
        split_size = 5*1024*1024-len(sig)
        fo = open(fp, "rb")
        size = os.path.getsize(fp)
        rs = {}
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**5))
        wlock = threading.Lock()
        now = time.time()
        def upload(start, content):
            while True:
                try:
                    r = create_scraper().post(self.mirror+"/upload", files={
                        "file": ("tmp.gif", sig+content)
                    })
                    rs[start//split_size] = r.content.decode()
                    break
                except:
                    time.sleep(5)
            with wlock:
                open("tmp.{}.json".format(now), "wb").write(json.dumps(rs).encode())
        for start in range(0, size, split_size):
            c = fo.read(split_size)
            tw.add(job=def_template(upload, start, c))
            while tw.alive_threads_ct>2**5:
                time.sleep(1)
        fo.close()
        tw.wait()
        if publish:
            rs = self.publish(rs, fo)
        return rs

    def publish(self, rs, fo):
        rs = {int(k): v for k, v in rs.items()}
        from .core import Telegraph
        tg = Telegraph()
        p=tg.p(tg.strong("Name: "))
        p.append(os.path.abspath(fo.name))
        p=tg.p(tg.strong("Size: "))
        p.append(str(os.path.getsize(fo.name)))
        ks = sorted(list(rs.keys()))
        for k in ks:
            v = rs[k]
            v = json.loads(v)[0]["src"]
            p=tg.p(tg.strong("part {}: ".format(k)))
            p.append(tg.a(self.mirror+v, "link"))
        return tg.publish()

    def download(self, url_or_json, fp):
        split_size = 5 * 1024 * 1024 - len(sig)
        r = url_or_json
        if isinstance(r, str):
            r = create_scraper().get(r)
            r = html.fromstring(r.content.decode())
            r = [_ for _ in r.xpath("//article//a/@href") if _.startswith("/file/")]
            r = {i: self.mirror+v for i, v in enumerate(r)}
        else:
            for k in list(r.keys()):
                r[k] = self.mirror + json.loads(r[k])[0]["src"]
        ks = sorted(list(r.keys()))
        r = {int(k): v for k, v in r.items()}
        fo = open(fp, "wb+")
        tw = threadwrapper.ThreadWrapper(threading.Semaphore(2**5))
        wlock = threading.Lock()
        def download(k, url):
            while True:
                try:
                    c = create_scraper().get(url).content[41:]
                    break
                except:
                    time.sleep(5)
            with wlock:
                print(k, k*split_size, len(c))
                fo.seek(k*split_size)
                fo.write(c)
        if len(ks)==1:
            size = int(create_scraper().head(r[ks[0]]).headers["Content-Length"])
        else:
            r0 = create_scraper().get(r[ks[-1]])
            size = int(len(r0.content))
        size = split_size*(len(ks)-1)+size-len(sig)
        # print(size)
        # raise
        fo.seek(size - 1)
        fo.write(b"\0")
        fo.seek(0)
        for k in ks:
            v = r[k]
            tw.add(job=def_template(download, k, v))
            while tw.alive_threads_ct>2**5:
                time.sleep(1)
        tw.wait()
        fo.close()



