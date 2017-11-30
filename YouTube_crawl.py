# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 10:02:17 2017

@author: 吴聪
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def download(url):#download the html
    header_fox={
            'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Cookie':'__cfduid=d1b3897e61f5309a2316b…lblade=1; _gat_curseTracker=1',
            'Host':'socialblade.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0'}
    print('process is downloading %s'%url )
    req=requests.get(url)  
    req.encoding='utf-8'
    return req.text

#解析得到每一个视频列表
def get_url_index(html_index):
    href_list=[]
    name_list=[]
    grad_list=[]
    soup=BeautifulSoup(html_index,'lxml')
    grad_nodes=soup.find_all('div',style="float: left; width: 70px; font-size: 1.1em;")
    for grad_node in grad_nodes:
        grad_list.append(grad_node.getText().lstrip('\n'))
    nodes=soup.find_all('div',style="float: left; width: 350px; line-height: 25px;")
    for node in nodes:
        href_c=node.find('a')
        href_list.append('https://socialblade.com'+href_c['href'])
        name_list.append(href_c.string)
    return href_list,name_list,grad_list

#解析视频网站
def get_video_url(html_detail):
    
    video_list=[]
    soup=BeautifulSoup(html_detail,'lxml')
    node=soup.find('a',class_="core-button -margin core-small-wide ui-black")['href']
    type_node=soup.find('a',id="youtube-user-page-channeltype").string
    return node,type_node


if __name__=="__main__":
    urls_index=['https://socialblade.com/youtube/top/country/tw',
    'https://socialblade.com/youtube/top/country/sa',
    'https://socialblade.com/youtube/top/country/ae',
    'https://socialblade.com/youtube/top/country/eg',
    'https://socialblade.com/youtube/top/country/mx',
    'https://socialblade.com/youtube/top/country/cl',
    'https://socialblade.com/youtube/top/country/ru',
    'https://socialblade.com/youtube/top/country/ua']
    for url_index in urls_index:
        file_name=url_index.split('/')[-1]
        print('begin to download %s'%url_index)
        html_cont=download(url_index)
        href_list,name_list,grad_list=get_url_index(html_cont)
        video_list=[]
        class_list=[]
        i=1
        for href in href_list:
            print('%s href %s:%s'%(file_name,i,href))
            html_detail=download(href)
            video_url,classType=get_video_url(html_detail)
            video_list.append(video_url)
            class_list.append(classType)
            i+=1
        sourceList={'name':name_list,'grad':grad_list,'type':class_list,'url':video_list}
        sourceList=pd.DataFrame(sourceList)
        sourceList.to_excel('%s.xlsx'%file_name,index=False)
    