# coding: utf8
"""
This module is designed for parse the weather data
"""
import requests
from bs4 import BeautifulSoup, Tag
from api.city.main import Transmitter
from api.config.config import Config

import json


class WeatherAPI:
    def __init__(self):
        self.session = requests.Session()

        self.config = Config()
        self.trans = Transmitter()

    def getWeather(self, name):
        cities_info = self.trans.cityCode(u'聊城')
        if len(cities_info) == 0:  # 没有查询到城市
            # TODO 抛出错误提示
            raise RuntimeError(u'There is no city named %s.' % name)
        elif len(cities_info) == 1:  # 只查询到一个城市
            code = cities_info[0][3]
        else:  # 查询到多个城市
            # TODO 提示用户选择,这里先简单取第一个
            code = cities_info[0][3]

            pass

        data = {u'id': code}

        response = self.session.post(self.config.getWeatherCNUrl(), data=data)
        soup = BeautifulSoup(response.content, u'html.parser')
        # print(soup.prettify())
        # print(soup.title)
        # table_tag = soup.find_all(u'table', class_=u'sevendays')[0]
        table_tag = soup.find(u'table', class_=u'sevendays')

        data = list()
        for child in table_tag.children:
            if not isinstance(child, Tag):
                continue

            date = child.find(u'td', class_=u'date').get_text()
            temp = child.find(u'td', class_=u'temp').get_text()
            desc = child.find(u'td', class_=u'desc').get_text()

            date = u''.join(date.split())
            temp = u''.join(temp.split())
            desc = u''.join(desc.split())

            data.append({u'date': date, u'temp': temp, u'desc': desc})

            # print(''.join(date.split()))
            # print(''.join(temp.split()))
            # print(''.join(desc.split()))
            # print(u'=================')
        return data

    @staticmethod
    def _parse(html):
        """
        <ul class="earlywarning"> 包含天气预警
        <div class="header-info"> 包含当前天气信息
        <table class="sevendays"> 默认 7 天的天气

        :param html: html data.
        :return: json data with weather info.
        """
        soup = BeautifulSoup(html, u'html.parser')
        soup.find(u'table', class_=u'sevendays')


if __name__ == '__main__':
    api = WeatherAPI()
    api.getWeather('丰台')
