# -*- coding: utf-8 -*-
import json
import os
import re

import botpy
import requests
from botpy import logging
from botpy.message import Message
from botpy.ext.cog_yaml import read
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


# 请求获取答案
def resopenai(scont):
    url = test_config["url"]
    data = {'prompt': scont}
    headers = {'Content-Type': 'application/json'}

    # 发送 API 请求并获取响应内容
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        # 处理响应结果：将所有聊天消息放入一个列表中，并取出最后一条消息
        chat_messages = []
        for line in response.iter_lines():
            if line:
                chat_message = json.loads(line)
                chat_messages.append(chat_message)
        last_message = chat_messages[-1]
        text = last_message['text']
        return text
    else:
        # 处理请求错误信息
        print(f'Request failed with code {response.status_code}')
        return "Get the error！"


# 转化成图片
def getpr(context):
    # 配置字体和空白边缘大小
    font_size = 50
    padding = 50

    # 加载自定义字体文件
    font = ImageFont.truetype("AlibabaPuHuiTi-2-35-Thin.ttf", size=font_size)

    # 计算文本的宽度和高度
    dummy_img = Image.new('RGB', (0, 0))
    draw = ImageDraw.Draw(dummy_img)
    text_width, text_height = draw.textbbox((0, 0), context, font=font)[2:]

    # 根据文本的宽度和高度调整图像大小
    image_width = text_width + padding * 2
    image_height = text_height + padding * 2

    # 创建一个空白图像，并在其中绘制文本
    image = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(image)
    draw.text((padding, padding), context, font=font, fill='black')

    # 将生成的图像以二进制格式存储在内存中
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_bytes = buffered.getvalue()
    return img_bytes


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        # 去掉前面的@消息
        pattern = r"<@!\d+>"
        # 获取文字
        clean_message = re.sub(pattern, "", message.content)
        # 去掉前面的空格
        msg = clean_message.lstrip()
        # 发送请求
        repos = resopenai(msg)
        print(repos)
        imby = getpr(repos)
        # 通过api发送回复消息
        await self.api.post_message(
            channel_id=message.channel_id,
            msg_id=message.id,
            content=f"<@!{message.author.id}>:【{msg}】",
            file_image=imby
        )


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], token=test_config["token"])
