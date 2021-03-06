# -*- coding: utf-8 -*-
"""
Created on 2019-10-27 11:21:35

author: huangyunbin

email: huangyunbin@sina.com

QQ: 592440193

bad news 利空走势分析Analysis on the trend of bad news
分析方法：利空点前三个月的高点，后三个月的低点，低点后一个月反弹的高点
"""

import pandas as pd
from numpy import NaN as npNaN
from math import isnan
import dateutil.parser


def idxmax(ds, i, j):
    '''
    返回pandas.Series指定位置、指定区间内的最大值及索引
    返回的是pandas.Series，只有一行，当有多个相同最大值时
    返回的是前面的那个
    注意：ds索引号为顺序号，l>0
    '''
    if isnan(i):
        return None
    if (j <= 0) | ((i - j + 1) < 0) | (i > len(ds)):
        return None
    s = ds.iloc[(i - j + 1): i + 1]
    return s.loc[[s.idxmax()]]


def idxmin(ds, i, j):
    '''
    返回pandas.Series指定位置、指定区间内的最小值及索引
    返回的是pandas.Series，只有一行，当有多个相同最小值时
    返回的是前面的那个
    注意：ds索引号为顺序号，l>0
    '''
    if isnan(i):
        return None
    if (j <= 0) | ((i - j + 1) < 0) | (i > len(ds)):
        return None
    s = ds.iloc[(i - j + 1): i + 1]
    return s.loc[[s.idxmin()]]


def badnews(df, date, j=60, k=60, n=30, m=120):
    '''
    利空走势分析：利空发生日前j个交易日内（含消息日）高点，
    利空发生日后k个交易日内（不含消息日）低点
    低点后n个交易日内（不含低点日）高点
    利空发生日后m个交易日内（含消息日）低点和高点
    '''
    df = df.sort_index()  # 按索引date排序
    dt = dateutil.parser.parse(date)
    idxname = df.index.name  # 获取所有名，所有名一般为date
    df = df.reset_index()  # 将索引date变成一列
    i = df.loc[(df[idxname] > dt)].index[0] - 1  # 对应索引序号
    # 由于有可能日期不在序列中，所以要用“>”
    # -1 表示事件发生日前一交易日
    p = df.loc[i, 'close']  # 对应收盘价
    dt = df[idxname].iloc[i].strftime('%Y%m%d')
    ds = df['close']
    if i < j - 1:  # 前面交易天数不够
        j = i + 1
    p0 = idxmax(ds, i, j)  # 获取前高点信息
    p0i = p0.index[0]  # 前高点索引序号
    p0v = p0.loc[p0i]  # 前高点价格
    p0d = df[idxname].iloc[p0i].strftime('%Y%m%d')  # 前高点日期
    p0ds = i - p0i   # 距前高点交易日天数
    p0zf = p / p0v - 1  # 前期跌幅
    if i + k > len(ds):  # 后面交易天数不够
        k = len(ds) - 1 - i
    p1 = idxmin(ds, i + k, k)  # 获取后低点信息
    p1i = p1.index[0]
    p1v = p1.loc[p1i]
    p1d = df[idxname].iloc[p1i].strftime('%Y%m%d')
    p1ds = p1i - i
    p1zf = p1v / p - 1
    p1zf_max = p1v / p0v - 1  # 从半年多前最高到此低点的跌幅
    if p1i + n > len(ds):  # 后面天数不够
        n = len(ds) - 1 - p1i
    p2 = idxmax(ds, p1i + n, n)
    if p2 is not None:
        p2i = p2.index[0]
        p2v = p2.loc[p2i]
        p2d = df[idxname].iloc[p2i].strftime('%Y%m%d')
        p2ds = p2i - i
        p2zf = p2v / p1v - 1
    else:
        p2i = None
        p2v = None
        p2d = None
        p2ds = None
        p2zf = None
    if i + m > len(ds):  # 后面交易天数不够
        m = len(ds) - 1 - i
    p3 = idxmin(ds, i + m, m)  # 获取后低点信息
    p3i = p3.index[0]
    p3v = p3.loc[p3i]
    p3d = df[idxname].iloc[p3i].strftime('%Y%m%d')
    p3ds = p3i - i
    p3zf = p3v / p - 1

    p4 = idxmax(ds, i + m, m)  # 获取后高点信息
    p4i = p4.index[0]
    p4v = p4.loc[p4i]
    p4d = df[idxname].iloc[p4i].strftime('%Y%m%d')
    p4ds = p4i - i
    p4zf = p4v / p - 1

    return [p0d, p0ds, p0v, p0zf, 
            dt, p,
            p1d, p1ds, p1v, p1zf, p1zf_max,
            p2d, p2ds, p2v, p2zf,
            p3d, p3ds, p3v, p3zf,
            p4d, p4ds, p4v, p4zf]

