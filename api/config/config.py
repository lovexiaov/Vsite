# -*- coding: utf-8 -*-
"""
此模块用于读取工程配置文件
"""
__author__ = 'lovexiaov'

import os.path as p
import configparser as parser
from api.common.const import PROJECT_ABSPATH

conf_path = p.join(p.dirname(p.realpath(__file__)), r'cfg.ini')


class Config(object):
    def __init__(self):
        self.parser = parser.ConfigParser()
        self.parser.read(conf_path, encoding=u'utf-8')

    def getCityDBPath(self):
        """
        :return: 数据库基于项目根目录的相对路径
        """
        return p.join(PROJECT_ABSPATH, self._get('city', 'db_path'))

    def getWeatherCNUrl(self):
        return self._get('cnweather', 'weather')

    def _get(self, category, key):
        return self.parser.get(category, key)

    def end(self):
        self.parser.clear()


def _main():
    config = Config()
    db_path = config.getCityDBPath()
    print(db_path)
    config.end()


if __name__ == '__main__':
    _main()
