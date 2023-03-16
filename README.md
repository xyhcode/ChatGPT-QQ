# ChatGPT-QQ-Bot

#### 介绍
QQ机器人接入ChatGPT


#### 安装教程
下载包(部分)
```shell
pip install qq-botpy

# 需要开代理
pip install pillow
```

修改配置文件`config.yaml`
```yaml
# qq机器人appid
appid: "xxxx"
# qq机器人token
token: "xxx"
# 请求openai 地址
url: "xxxx"
```

### 参考
[QQ机器人](https://bot.q.qq.com/wiki/develop/pythonsdk/)

### 说明
发送指令回复
```shell
@机器人 问题
```
机器人回复的是图片，因为官方的访问，只要内容包含斜杠一类的就会被视为链接，直接无法发送，使用此示例获取到要发送的内容后，会生成图片，然后发送给用户