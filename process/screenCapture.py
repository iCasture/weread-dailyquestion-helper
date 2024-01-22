# -*- coding: utf-8 -*-

from base64 import b64encode
from io import BytesIO

from PIL import ImageGrab

# 这里用 "MINI_APP" 即可
# mode = 'JIE_TU'
mode = "MINI_APP"

# FRIEND_PK 是 '问答 PK 模式'; SELF_PK 是 '每日一答' 模式
# type = "FRIEND_PK"
type = "SELF_PK"


class screenCapture:
    def __init__(self, positionDebug=False):
        self.positionDebug = positionDebug

        if mode == "JIE_TU":
            # 截图顶点调试 (x1, y1, x2, y2)
            self.bound = (0, 90, 0 + 415, 90 + 725)
        else:
            # 笔记本小程序顶点截图 (x1, y1, x2, y2)
            # self.bound = (35, 63, 35 + 420, 63 + 785)
            self.bound = (35, 30, 35 + 420, 30 + 785)

        self.rpx = self._rpx2px(self.bound[2] - self.bound[0])

    # rpx 转 px
    def _rpx2px(self, base):
        ratio = base / 750

        def _rpx(rpx):
            return rpx * ratio

        return _rpx

    # 截图
    def _getCapture(self):
        img = ImageGrab.grab(self.bound)
        return img

    # base64
    def base64(self, img):
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img.close()

        b64_str = b64encode(buffer.getvalue())

        return b64_str

    # 切割
    def _splitCapture(self, img):
        if type == "FRIEND_PK":
            # 笔记本好友 PK
            questionImg = img.crop(
                (self.rpx(85), self.rpx(580), self.rpx(585), self.rpx(580 + 130))
            )
            optionsImg = img.crop(
                (self.rpx(85), self.rpx(710), self.rpx(585), self.rpx(710 + 465))
            )
        if type == "SELF_PK":
            # 笔记本每日一答
            questionImg = img.crop(
                (self.rpx(85), self.rpx(440), self.rpx(85 + 585), self.rpx(440 + 130))
            )
            optionsImg = img.crop(
                (self.rpx(85), self.rpx(570), self.rpx(85 + 585), self.rpx(570 + 465))
            )

        # 供 macOS 下调试窗口大小与位置用
        if self.positionDebug:
            img.save("output/images/all.png")
            questionImg.save("output/images/questionImg.png")
            optionsImg.save("output/images/optionsImg.png")

        return questionImg, optionsImg, img

    def run(self, positionDebug=False):
        self.positionDebug = positionDebug
        img = self._getCapture()
        return self._splitCapture(img)
