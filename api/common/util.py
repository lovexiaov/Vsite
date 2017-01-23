# -*- coding: utf-8 -*-
__author__ = 'lovexiaov'


def group(seq):
    """
    将 list 或 tuple 中的元素组合成一个字符串
    :param seq:
    :return: 组合字符串
    """
    if not (isinstance(seq, list) or isinstance(seq, tuple)):
        raise RuntimeError('Only support list and tuple.')
    result = ''
    for i in seq:
        result += i

    return result


if __name__ == '__main__':
    # print(group('hello'))
    print(group(('hello', 'world')))
    # print(group({'1': 'hello', '2': 'world'}))
