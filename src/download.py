import os
import requests
import html2text
from bs4 import BeautifulSoup
import re
from random import choice
# import configure
import tomd


# header = {}
# header['user-agent'] =  choice(Configure.FakeUserAgents)

test_url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1577605723&ver=2063&signature=9zYwrSl771SsNT7qx4GYDFQ3yCdUXZOIJ5ztwlih4myfqZ9suV24p6RwR5KtTdMqkHhUSuAqo-uPh*EtXfhD*9hAc-x8hQP-FUPlYVAUHxvotU7QLpoD4sWgNtbmFEaV&new=1'


def get_content(url):

    try:
        response = requests.get(url)
        content = None

        if response.status_code == requests.codes.ok:
            content = response.text
            
    except Exception as e:
        print(e)

    soup = BeautifulSoup(content, 'lxml')
    html_content = soup.find(id="img-content")
    
    title = html_content.find(class_='rich_media_title')
    # title.string = title.text.strip()
    # title = html_content.h2.text.strip()
    title.string = re.match(r'论文浅尝 \| (.*)', title.text.strip()).group(1)

    filename = title.text.strip().replace(' ','-') + '.md'

    publish_time = html_content.find(id='meta_content').em.text.strip()

    author = html_content.find(id='meta_content').find('span',attrs={'class': 'rich_media_meta rich_media_meta_text'}).text
    author = author.strip()

    # html_content.find(id='activity-name').decompose()
    html_content.find(id='meta_content').decompose()

    # new_tag = html_content.new_tag('h1')
    # new_tag.string = title

    new_tag = soup.new_tag('p')
    new_tag.string = "> 笔记整理: " + author
    title.insert_after(new_tag)

    # 处理图片
    ## 文件夹
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = dir_path + "/posts/%s" % title.text.strip()
    dir_img = dir_name + "/img"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
        os.mkdir(dir_img)

    
    ## 下载并替换为本地图片
    counter = 1
    
    images = html_content.find_all('img')

    if images:
        for image in images:
            img_src = image.get('data-src')
            img_type = image.get('data-type')
            img_name = "{0:s}_{1:d}.{2:s}".format(filename, counter, img_type if img_type else 'png')
            counter += 1

            file_path = dir_img + '/' + img_name
            print(file_path)
            with open (file_path, 'wb') as file:
                response = requests.get(url = img_src)
                for block in response.iter_content(1024):
                    if block:
                        file.write(block)
                    else:
                        break
            tag = soup.new_tag('span')
            tag.string = "![](img/{0:s})".format(img_name)
            image.replace_with(tag)
            
    # 去除<br/> <br></br>
    brs = html_content.find_all('br')
    if brs:
        for br in brs:
            br.decompose()

    mdText = str(html_content).replace('<br/>','')

    pattern = re.compile('OpenKG.CN(.*)', re.MULTILINE)
    mdText = pattern.sub('', mdText)

    mdText = tomd.Tomd(mdText).markdown

    with open(dir_name + '/' +filename, 'w', encoding='utf8') as file:
        file.write(mdText)
    
    return title, publish_time, author


def get_urls():
    url = "http://weixin.sogou.com/weixin"
    try:
        response = requests.get(url, headers=header, params=payload)
        content = None

        if response.status_code == requests.codes.ok:
            content = response.text
            
    except Exception as e:
        print (e)

    soup = BeautifulSoup(content, 'lxml')

    news_list = soup.find(class_='news-list').find_all('li')

    for new in news_list:
        get_content(new.a.get('href').strip())
        #break



if __name__ == '__main__':
    title, publish_time, author = get_content(test_url)
    print(title)
    print(publish_time)
    print(author)

