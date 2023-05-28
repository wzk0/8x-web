import requests
from bs4 import BeautifulSoup
import json

headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}

domain="https://8vcsh.top"
update="https://github.com/8xx8x/8x8x"

def req(link):
    r=requests.get(link,headers=headers)
    soup=BeautifulSoup(r.text,features='html5lib')
    return soup

def analysis_page(page):
    if int(page)==1:
        soup=req(domain+'/video/')
    else:
        soup=req(domain+'/video/page/%s/'%page)
    all_info=[]
    for li in soup.find_all('li'):
        if '点击在线播放' in str(li): 
            all_info.append({'name':li.find('p').text,'pic':li.find('img')['data-src'],'vid':li.find('a')['href'].split('/')[-2]})
    return all_info

def analysis_video(vid):
    soup=req('https://8vcsh.top/video/%s/'%vid)
    def give_me_soup(soup):
        for div in soup.find_all('div'):
            if '下载观看' in str(div):
                return div
    div=give_me_soup(soup)
    for a in div.find_all('a'):
        if '下载观看' in str(a):
            download=a['href']
    for h1 in soup.find_all('h1'):
        if 'lhgt' in str(h1):
            name=h1.text
    return {'name':name,'pic':soup.find('video')['poster'],'download':download}

def search(word,page):
    r=requests.post('https://s.%s/search'%domain.replace('https://',''),headers={'Content-type':'application/x-www-form-urlencoded'},data={'title':str(word),'current':str(page),'size':'16','source':'v1'})
    data=json.loads(r.text)
    return data['data'],data['totalPage'],data['page']