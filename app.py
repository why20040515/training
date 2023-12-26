import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Bar, Scatter, Funnel, PictorialBar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import WordCloud
import streamlit as st
import streamlit_echarts
import re
import time


def rm(s):
    return re.sub(r'[^\u4e00-\u9fa5]', '', s)


# 取词频前20个

n = 20

# 数据处理
def data(items):
    word_counts = Counter()
    for item in items:
        words = jieba.cut(rm(item.text))
        words = [s for s in words if len(s) != 1]
        word_counts.update(words)
    return word_counts


# 生成柱状图
def paint_bar(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    bar = Bar()
    bar.add_xaxis(list(word_counts.keys())[:n])
    bar.add_yaxis("词频", list(word_counts.values())[:n])
    bar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)))
    streamlit_echarts.st_pyecharts(bar, height='400px')


# 生成线形图
def paint_line(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    line = Line()
    line.add_xaxis(list(word_counts.keys())[:n])
    line.add_yaxis("词频", list(word_counts.values())[:n])
    line.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)))
    streamlit_echarts.st_pyecharts(line, height='400px')


# 生成散点图
def paint_scatter(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    scatter = Scatter()
    scatter.add_xaxis(list(word_counts.keys())[:n])
    scatter.add_yaxis("词频", list(word_counts.values())[:n])
    scatter.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)))
    streamlit_echarts.st_pyecharts(scatter, height='400px')


# 生成象形柱图
def paint_pictorialBar(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    pictorialBar = PictorialBar()
    pictorialBar.add_xaxis(list(word_counts.keys())[:n])
    pictorialBar.add_yaxis("词频", list(word_counts.values())[:n])
    pictorialBar.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)))
    streamlit_echarts.st_pyecharts(pictorialBar, height='400px')


# 生成饼状图
def paint_pie(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    pie = Pie()
    pie.add("", list(word_counts.items())[:n])
    streamlit_echarts.st_pyecharts(pie, height='600px')


# 生成词云图
def paint_wordcloud(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    wordcloud = WordCloud()
    wordcloud.add("单词频率", list(word_counts.items())[:n], word_size_range=[20, 80])
    streamlit_echarts.st_pyecharts(wordcloud, height='400px')


# 生成漏斗图
def paint_funnel(items):
    word_counts = data(items)
    word_counts = {k: v for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)}
    funnel = Funnel()
    funnel.add("单词频率", list(word_counts.items())[:n])
    streamlit_echarts.st_pyecharts(funnel, height='800px')


st.set_page_config(page_title="网站关键词出现频率）", page_icon="🐛", layout="wide")
st.sidebar.header("python爬虫")
selected_charts = st.sidebar.selectbox(
    "您希望以哪种图显示：",
    ("柱状图", "线形图", "饼状图", "词云图", "散点图", '漏斗图','象形柱图')
)
st.markdown("# 网站热词")
url = st.text_input('请输入你想爬取的网站的url')
if st.button('查询'):
    if url != '':
        resp = requests.get(url)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.content, 'html.parser')
        nav_items = soup.find_all('div')
        if nav_items == []:
            st.markdown("# :red[爬取失败，请输入其他url！]")
        else:
            if selected_charts == '柱状图':
                paint_bar(nav_items)
            elif selected_charts == '线形图':
                paint_line(nav_items)
            elif selected_charts == '饼状图':
                st.write("<h5>关键词出现频率饼状图</h5>", unsafe_allow_html=True)
                paint_pie(nav_items)
            elif selected_charts == '词云图':
                paint_wordcloud(nav_items)
            elif selected_charts == '散点图':
                paint_scatter(nav_items)
            elif selected_charts == '漏斗图':
                paint_funnel(nav_items)
            elif selected_charts == '象形柱图':
                paint_pictorialBar(nav_items)
    else:
        st.markdown(':red[请输入网址]')
