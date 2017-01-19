# coding: utf8
"""
This module is designed for parse the weather data
"""
import requests
from bs4 import BeautifulSoup, Tag
from city.main import Transmitter


class WeatherAPI:
    def __init__(self, config):
        self.session = requests.Session()

        self.config = config
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
        table_tag = soup.find_all(u'table', class_=u'sevendays')[0]

        for child in table_tag.children:
            if not isinstance(child, Tag):
                continue

            date = child.find(u'td', class_=u'date').get_text()
            temp = child.find(u'td', class_=u'temp').get_text()
            desc = child.find(u'td', class_=u'desc').get_text()
            print(''.join(date.split()))
            print(''.join(temp.split()))
            print(''.join(desc.split()))
            print(u'=================')
            # return response.content


if __name__ == '__main__':
    from config.config import Config

    api = WeatherAPI(Config())
    api.getWeather('聊城')
