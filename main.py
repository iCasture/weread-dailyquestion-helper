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
    questionImg, optionsImg = None, None
    tmpQuestionText = ""

    while True:
        tmpQuestionImg, tmpOptionsImg, appImg = screenCapture().run()

        # print(tmpQuestionImg)
        # print(tmpOptionsImg)

        if not isSame(questionImg, tmpQuestionImg):
            questionImg, optionsImg, appImg = tmpQuestionImg, tmpOptionsImg, appImg
            config = getOCRConfig()
            question, options = OCR(
                config["APP_ID"], config["API_KEY"], config["SECRET_KEY"]
            ).run(questionImg, optionsImg)

            # 如果匹配到 victory / defeat 则退出程序
            if re.search(
                "victory|defeat|defert|自动匹配|排行榜|看广告", "".join(options), flags=re.I
            ):
                sys.exit()

            if len(question) > 0 and (tmpQuestionText != question):
                tmpQuestionText = question

                freq, rightOption, hint = Query().run(question, options)

                if rightOption is not None:
                    print("问题: {}".format(question))
                    print("\033[1;47;32m正确答案: {}\033[0m".format(rightOption))
                    freqText = ""
                    for index in range(len(freq)):
                        freqText += (
                            options[index]
                            + " :"
                            + str(round(100 * freq[index], 1))
                            + "%    "
                        )
                    print("概率: {}".format(freqText))
                    print("依据: {}".format(hint))

                    if isAutoClick:
                        autoClick(0, 40).run(appImg, options, rightOption)

                    print("-----------------")
                    print()

        # 暂停 100ms
        time.sleep(0.1)
