# -*- coding: utf-8 -*-
__author__ = 'lovexiaov'

import sqlite3
from config.config import Config

config = Config()


class Transmitter(object):
    def __init__(self):
        self.db = sqlite3.connect(config.getCityDBPath())

    def listProvince(self, count=-1):
        """
        :param count: 列出的个数, 默认值为 -1,即列出所有省份名称
        :return: 省份名称列表
        """
        sql = u'SELECT name FROM province LIMIT %s;' % count
        cursor = self._query(sql)
        return map(lambda x: x[0], cursor.fetchall())

    def cityCode(self, name):
        """
        通过城市名称查询其天气代码
        :param name: 城市名称
        :return: e.g. [('北京', '朝阳', '朝阳', '101010300'),('辽宁', '朝阳', '朝阳', '101071201')]
        """
        sql = u'''SELECT
                    p.name,
                    c.name,
                    d.name,
                    d.code
                  FROM province p, city c, district d
                  WHERE d.name = "{}" AND c._id = d.city_id AND p._id = c.prov_id;'''.format(name)

        return list(self._query(sql).fetchall())

    def _query(self, sql):
        # TODO 校验 sql 语句, 防止 sql 注入
        return self.db.execute(sql)

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.db.close()


if __name__ == '__main__':
    # 查询器
    trans = Transmitter()
    # provs = trans.listProvince(66)
    # for prov in provs:
    #     # print(type(prov))
    #     print(prov)

    # trans.listCity(1)
    # trans.listDistrict(1)

    for cityinfo in trans.cityCode("朝阳"):
        print(cityinfo)

    trans.close()
