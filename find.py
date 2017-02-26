#!/usr/bin/python

# Script        : 搜索企业负责人
# Author        : ghost
# Description   : tianyancha爬虫 获取给出的一个企业负责人的关系网

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import re

domain="http://www.tianyancha.com"
start_url="{}/human/2065961364-c651442".format(domain)
POOL=[]


# Main
# TODO :: 存储在redis中
def find_loop(start_url):
    result=parse_page_result(start_url)
    info=result.get('info')
    related=result.get('related')
    for name,link in related.items():
        if is_never_searched(link):
            if is_matched(info,parse_page_result(link).get('info')):
                print("{} 可能认识 {} Url::{}".format(info['name'],name,link))
                POOL.append(link)
                find_loop(link)


# 解析页面的信息
def parse_page_result(url):

    html=_load_dynamically_url(url)
    bs=BeautifulSoup(html,"lxml")
    result={
        "related":_get_related(bs),
        "info":_get_info(bs)
    }

    return result


# 检查目标地址是否已经被搜索
def is_never_searched(link):
    if link in POOL:
        return False
    else:
        return True


# TODO 多维度匹配检测 
def is_matched(info_a,info_b):
    return True


# 获取可能认识的人
def _get_related(bs):
    related={}
    found=bs.find_all(href=re.compile('human'))

    for human in found:
        name=human.get_text()
        link="{}{}".format(domain,human['href'])
        related[name]=link

    return related


# 获取个人信息
def _get_info(bs):
    info={}
    # name=bs.select('div.f16.ng-binding')

    result=bs.find_all('div',{'class':'f16 ng-binding'})
    if result is not None:
        try:
            name=result[0].get_text()
            info['name']=name
        except:
            info={}
    return info


# 执行页面获取结果
def _load_dynamically_url(url):
    browser = webdriver.PhantomJS(service_args=['--load-images=no'])
    browser.get(url)
    element = browser.find_element_by_xpath('/html/body')
    html= element.get_attribute('innerHTML')
    return html

# 生成关系画像数据
def _gen_profile(start_url):
    pass


if __name__=='__main__':
    find_loop(start_url)
