# -*- coding: utf-8 -*-

import re
import sys
import time

from PIL import ImageChops

from process.autoClick import autoClick
from process.OCR import OCR
from process.query import Query
from process.screenCapture import screenCapture
from process.util import getOCRConfig

# END_WORDS_DICT = {"VICTORY": True}
isAutoClick = False


def isSame(imgA, imgB):
    if imgA is None or imgB is None:
        return False
    diff = ImageChops.difference(imgA.convert("RGB"), imgB.convert("RGB"))
    if diff.getbbox():
        return False
    return True


if __name__ == "__main__":
    quesImg, answImg = None, None
    tmpQuesText = ""

    while True:
        tmpQuesImg, tmpAnswImg, appImg = screenCapture().run()

        # print(tmpQuesImg)
        # print(tmpAnswImg)

        if not isSame(quesImg, tmpQuesImg):
            quesImg, answImg, appImg = tmpQuesImg, tmpAnswImg, appImg
            config = getOCRConfig()
            ques, answ = OCR(
                config["APP_ID"], config["API_KEY"], config["SECRET_KEY"]
            ).run(quesImg, answImg)

            # 如果匹配到 victory / defeat 则退出程序
            if re.search(
                "victory|defeat|defert|自动匹配|排行榜|看广告", "".join(answ), flags=re.I
            ):
                sys.exit()

            if len(ques) > 0 and (tmpQuesText != ques):
                tmpQuesText = ques

                freq, rightAnswer, hint = Query().run(ques, answ)

                if rightAnswer is not None:
                    print("问题: {}".format(ques))
                    print("\033[1;47;32m正确答案: {}\033[0m".format(rightAnswer))
                    freqText = ""
                    for index in range(len(freq)):
                        freqText += (
                            answ[index]
                            + " :"
                            + str(round(100 * freq[index], 1))
                            + "%    "
                        )
                    print("概率: {}".format(freqText))
                    print("依据: {}".format(hint))

                    if isAutoClick:
                        autoClick(0, 40).run(appImg, answ, rightAnswer)

                    print("-----------------")
                    print()

        # 暂停 100ms
        time.sleep(0.1)
