# -*- coding: utf-8 -*-
import io

from aip import AipOcr


class OCR:
    def __init__(self, appId, apiKey, secretKey):
        self.client = AipOcr(appId, apiKey, secretKey)

    def _pil2bin(self, pilObj):
        bin = io.BytesIO()
        pilObj.save(bin, format="PNG")
        return bin.getvalue()

    def _ocr(self, img):
        imgBin = self._pil2bin(img)
        return self.client.basicGeneral(imgBin)

    def run(self, questionImg, optionsImg):
        question = self._ocr(questionImg)
        options = self._ocr(optionsImg)

        question = "".join([item["words"] for item in question["words_result"]])
        options = [item["words"] for item in options["words_result"]]

        return question, options
