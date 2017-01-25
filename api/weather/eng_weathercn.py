# coding: utf8
"""
This module is designed for parse the weather data
"""

import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup, Tag
from api.city.main import Transmitter
from api.config.config import Config
from api.common.util import group
from api.common.const import headers


class WeatherAPI:
    def __init__(self):
        self.session = requests.Session()

        self.config = Config()
        self.trans = Transmitter()

    def getWeather(self, name):
        cities_info = self.trans.cityCode(name)
        if len(cities_info) == 0:  # 没有查询到城市
            # TODO 抛出错误提示
            raise RuntimeError(u'There is no city named %s.' % name)
        elif len(cities_info) == 1:  # 只查询到一个城市
            code = cities_info[0][3]
        else:  # 查询到多个城市
            # TODO 提示用户选择,这里先简单取第一个
            code = cities_info[0][3]

        data = {u'id': code}

        response = self.session.post(self.config.getWeatherCNUrl(), data=data, headers=headers)
        # TODO 校验是否成功请求
        return self._parse(response.content)

    @staticmethod
    def _parse(html):
        """
        <ul class="earlywarning"> 包含天气预警
        <div class="header-info"> 包含当前天气信息
        <table class="sevendays"> 默认 7 天的天气
        :param html: html data.
        :return: json data with weather info.
        """
        result = dict()

        soup = BeautifulSoup(html, u'html.parser')
        # print(soup.prettify())

        # ==========城市名称
        name = group(soup.find(u'div', class_=u'logo-info').text.split())
        result['city'] = name.replace('更换城市', '')

        # ==========预警信息
        ul_warning = soup.find(u'ul', class_=u'earlywarning')
        result['warning'] = ul_warning.text.split() if ul_warning else []

        div_current = soup.find(u'div', class_=u'header-info')
        # ==========当前日期信息
        ptime = div_current.find(u'div', class_=u'curtime').text.split()[0]

        div_curdate = div_current.find(u'div', class_=u'curdate')
        curdate = div_curdate.get_text().split()

        result['date'] = curdate[0]
        result['weekday'] = curdate[1]
        result['lunar'] = curdate[2][2:]
        result['ptime'] = ptime

        # ==========当前天气信息
        div_curweather = div_current.find(u'div', class_=u'current-weather')

        curtemp = group(div_curweather.find(u'span', class_=u'cur-temp').text.split())
        tempscope = group(div_curweather.find(u'span', class_=u'temperature').text.split())
        desc = group(div_curweather.find(u'span', class_=u'description').text.split())

        result['curtemp'] = curtemp
        result['temp'] = tempscope
        result['desc'] = desc

        div_aqi = div_curweather.find(u'div', class_=u'aqi')
        if div_aqi:
            aqi = div_aqi.text.split()
            result['aqi'] = aqi[0]
            result['aqilevel'] = aqi[1]
        else:
            result['aqi'] = ''
            result['aqilevel'] = ''

        # ==========7日天气预报
        table_7days = soup.find(u'table', class_=u'sevendays')
        data_7days = list()
        for child in table_7days.children:
            if not isinstance(child, Tag):
                continue

            infos = child.text.split()
            data_7days.append({u'date': infos[0], u'temp': infos[1], u'desc': infos[2]})

        result['7days'] = data_7days
        # pprint(result)

        return result


if __name__ == '__main__':
    api = WeatherAPI()
    pprint(api.getWeather('闵行'))
    # html = open('statics/sample.html', 'r', encoding=u'utf-8')
    # WeatherAPI._parse(html.read())
    # html.close()
