# -*- coding: utf-8 -*-
import ssl
import time
from functools import reduce
from urllib import parse, request

from bs4 import BeautifulSoup

from process.util import getOCRConfig

ssl._create_default_https_context = ssl._create_unverified_context

# 搜索引擎配置, 支持 Google 以及百度
SEARCH_ENGINE = "GOOGLE"
# SEARCH_ENGINE = "BAIDU"

config = getOCRConfig()

# 如果需要手工指定 Google 的代理服务器地址, 请取消注释
# 并修改下面的代理地址
# if SEARCH_ENGINE == "GOOGLE":
#     httpproxy_handler = request.ProxyHandler(
#         {
#             "http": "127.0.0.1:1082",
#             "https": "127.0.0.1:1082",
#         }
#     )
#     opener = request.build_opener(httpproxy_handler)


class Query:
    def _getKnowledge(self, question):
        if SEARCH_ENGINE == "GOOGLE":
            url = "https://www.google.com/search?q={}".format(parse.quote(question))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "host": "www.google.com",
                "Cookie": config["GOOGLE_COOKIE"],
            }
        else:
            url = "https://www.baidu.com/s?wd={}".format(parse.quote(question))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "host": "www.baidu.com",
                "Cookie": config["BAIDU_COOKIE"],
            }
        req = request.Request(url, headers=headers)

        # 如果之前手工指定了 Google 的代理服务器, 那么用下面这几行
        # response = (
        #     opener.open(req) if SEARCH_ENGINE == "GOOGLE" else (request.urlopen(req))
        # )

        # 如果不需要手工指定 Google 的代理服务器, 那么用下面这一行
        response = request.urlopen(req)

        content = response.read().decode("utf-8")
        soup = BeautifulSoup(content, "html.parser")
        knowledge = soup.get_text()
        if "网络不给力，请稍后重试" in knowledge:
            time.sleep(0.5)
            print("怕不是被封了 …")
            return None
        return knowledge

    def _query(self, knowledge, options):
        freq = [knowledge.count(item) + 1 for item in options]
        rightOption = None
        hint = None

        if freq.count(1) == len(options):
            freqDict = {}
            for item in options:
                for char in item:
                    if char not in freqDict:
                        freqDict[char] = knowledge.count(item)
            for index in range(len(options)):
                for char in options[index]:
                    freq[index] += freqDict[char]
            rightOption = options[freq.index(max(freq))]
        else:
            rightOption = options[freq.index(max(freq))]
            threshold = 50  # 前后 50 字符
            hintIndex = max(knowledge.index(rightOption), threshold)
            hint = "".join(
                knowledge[hintIndex - threshold : hintIndex + threshold].split()
            )

        sum = reduce(lambda a, b: a + b, freq)
        return [f / sum for f in freq], rightOption, hint

    def run(self, question, options):
        if len(options) <= 0:
            return [], None, None
        knowledge = None
        while knowledge is None:
            knowledge = self._getKnowledge(question)
        try:
            freq, rightOption, hint = self._query(knowledge, options)
        except Exception as e:
            print("出现异常", e)
            freq, rightOption, hint = [], None, None
        return freq, rightOption, hint
