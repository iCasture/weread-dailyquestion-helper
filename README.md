# 微信读书每日一答辅助

## 功能描述

简单的说就是每隔一段时间截张图，去百度搜答案。支持自动点击正确答案（可选，在 `main.py` 中由 `isAutoClick` 配置，默认关闭）。

## 配置环境

- Python 3.11.7
- 微信 macOS 版
- 百度 AI 平台

## 原理

1. 截图；

2. OCR 识别问题和答案；

3. 根据问题去谷歌 / 百度搜答案；

    > 选择答案的依据是：以问题作为关键字进行搜索，在搜索结果的首页中，选择出现频率最高的答案选项作为候选结果，并把它的上下文作为「依据」，一并输出。

4. 自动寻找答案位置并作答；

    > 可选，在 `main.py` 中由 `isAutoClick` 配置，默认关闭。

5. 循环执行 1、2、3、4。

## 使用方法

1. 登陆 [百度 AI 开放平台](https://console.bce.baidu.com/ai/#/ai/ocr/app/list)，创建一个通用场景 OCR 应用（每天免费 10k 次够用了），并在应用列表中查看 `AppID`，`API Key` 和 `Secret Key`；

2. 打开 Google / 百度首页并登录，浏览器打开开发者工具，刷新页面，从网络请求头中找到 cookie 并复制；

    > 用 Google 做为搜索引擎的话需要 Google 的 cookie；用百度的话则需要百度的 cookie。

3. 在根目录下仿照 `config_demo.json` 创建一个 `config.json` 文件，把上面得到的值填进去；

4. 用 **电脑** 打开微信读书小程序，并 **保持在最前**，且不要被遮挡；

5. 运行根目录下的 `main.py` 文件；

6. 进入每日一答页面开始答题，隔一段时间控制台就会输出结果。

> 注：
>
> 1. 因为 macOS 没办法获取到小程序的窗口，所以需要手动测量小程序窗口大小，调整题目和答案位置。需要修改的参数位于 `process/screenCapture.py` 文件中。
>
>     调试方法：修改相应参数后，打开 Python 终端，执行 `from process.screenCapture import screenCapture`，然后再执行 `screenCapture().run(positionDebug=True)`。截图效果会输出在 `output/images` 目录下，可参考校对位置。
>
> 2. macOS 下需要在系统设置对执行 `main.py` 文件的 App 赋予「录屏」权限（例如 iTerm、VSCode 等），否则截图只能截取到桌面背景。参考：[PIL ImagineGrab only returns background image on Mac not a screen grab like I thought](https://stackoverflow.com/questions/67140184/pil-imaginegrab-only-returns-background-image-on-mac-not-a-screen-grab-like-i-th)。
>
> 3. 同时支持「每日一答」模式以及「问答 PK 模式」，需要在 `process/screenCapture.py` 文件中切换。
>
> 4. 搜索引擎支持 Google 以及百度，需要在 `process/query.py` 中手工切换。

## 效果示例

![1.png](./img/1.png)

![2.png](./img/2.png)

![3.png](./img/3.png)

![4.png](./img/4.png)

![5.png](./img/5.png)

![6.png](./img/6.png)

## 其它

仅供学习参考，正确率目测 80 ~ 90%，不是标准答案，不能保证完全正确。

目前的最大的瓶颈还是在于 **速度**，速度不够快即使答对了，也不能保证赢。**暂时也没有想到好的方案解决**。

```text
自动化答题总时间 = 截图时间 + OCR时间 + 搜索引擎查询时间 + 自动化答题时间
```

## 致谢
[@maotoumao](https://github.com/maotoumao)