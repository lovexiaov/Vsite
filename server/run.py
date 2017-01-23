# coding: utf-8
import os, sys

sys.path.append('/root/coding/Vsite')
# print(sys.path)
import json

from flask import Flask, request
from api.weather.eng_weathercn import WeatherAPI

app = Flask(__name__)


@app.route(u'/weather')
def hello():
    """
    接受 GET 请求，city=[城市名]
    :return: 指定城市的天气数据（json）
    """

    args = request.args  # ImmutableMultiDict([('city', '丰台'), ('arg2', 'hello')])
    city = args.get('city')
    if city:
        api = WeatherAPI()
        return result(api.getWeather(city))
    else:
        return result('', 'MUST HAVE param `city` not found.', 601)


def result(content, msg='Success', code=200):
    """
    将需要返回的信息组合成 json 字符串，并返回。
    :param content: 返回客户端的内容(str)
    :param msg: 状态消息(str)
    :param code: 状态码(int)
    :return: json 格式的字符串
    """
    return json.dumps({'code': code, 'msg': msg, 'content': content}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
