import os
import requests
import html2text
from bs4 import BeautifulSoup
import re
from random import choice
# import Configure
import tomd
import json
from fake_useragent import UserAgent

ua = UserAgent()

header = {}
header['user-agent'] =  'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

test_url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1577605723&ver=2063&signature=9zYwrSl771SsNT7qx4GYDFQ3yCdUXZOIJ5ztwlih4myfqZ9suV24p6RwR5KtTdMqkHhUSuAqo-uPh*EtXfhD*9hAc-x8hQP-FUPlYVAUHxvotU7QLpoD4sWgNtbmFEaV&new=1'

def read_paper_list():
    with open('./article.json', 'r', encoding='utf8') as file:
        paper_json = json.loads(file.read())
        # print(paper_json)
        paper_list = paper_json['paper']
    return paper_list


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
    print(title.text.strip())

    filename = title.text.strip().replace(' ','-') + '.md'

    publish_time = html_content.find(id='meta_content').em.text.strip()

    author = html_content.find(id='meta_content').find('span',class_='rich_media_meta')
    author = author.text.strip()[3:] if author else None
    
    # author = html_content.find(id='meta_content').find('span',attrs={'class': 'rich_media_meta rich_media_meta_text'}) #.text
    print(author)
    # author = author.strip()

    # html_content.find(id='activity-name').decompose()
    html_content.find(id='meta_content').decompose()

    # new_tag = html_content.new_tag('h1')
    # new_tag.string = title

    new_tag = soup.new_tag('p')
    new_tag.string = "> 笔记整理: " + author
    title.insert_after(new_tag)

    # image
    ## dir
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = dir_path + "/posts/%s" % title.text.strip()
    dir_img = dir_name + "/img"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
        os.mkdir(dir_img)

    ## download
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
            
    # delete <br/> <br></br>
    brs = html_content.find_all('br')
    if brs:
        for br in brs:
            br.decompose()

    mdText = str(html_content).replace('<br/>','')

    pattern = re.compile('^OpenKG(.*)', re.MULTILINE)
    mdText = pattern.sub('', mdText)

    mdText = tomd.Tomd(mdText).markdown

    with open(dir_name + '/' +filename, 'w', encoding='utf8') as file:
        file.write(mdText)
    
    write_to_summary(title.text.strip(), 'src/posts/{title}/{filename}'.format(title=title.text.strip(),filename=filename))
    write_to_acknowledge(author)
    return title.text, author


def get_urls():
    payload = {}
    page_num = 1

    for i in range(1, page_num+1):
        payload = {
            'type':2,
            's_from':'input',
            'query':'论文浅尝',
            'ie':'utf8',
            'page': i
        }

        url = "https://weixin.sogou.com/weixin"
        
        try:
            response = requests.get(url, headers=header, params=payload)
            content = None

            if response.status_code == requests.codes.ok:
                content = response.text
                
        except Exception as e:
            print (e)

        soup = BeautifulSoup(content, 'lxml')

        news_list = soup.find(class_='news-list').find_all('li')
        print('https://weixin.sogou.com/' + news_list[1].a.get('href').strip())
        get_content('https://weixin.sogou.com/' + news_list[1].a.get('href').strip())
        # for new in news_list:
        #     # get_content(new.a.get('href').strip())
        #     print(new.a.get('href').strip())


def write_to_summary(title, dir):
    with open( '../SUMMARY.md' , 'a', encoding='utf8') as file:
        file.write('- [{title}]({dir})\n'.format(title=title,dir=dir))
    print('write to summary...')

def write_to_acknowledge(author):
    with open( '../acknowledgement.md' , 'a', encoding='utf8') as file:
        file.write('- %s\n' % author)

if __name__ == '__main__':
    paper_list = read_paper_list()
    i = 0
    for url in paper_list[26:]:
        print(url)
        print(i)
        i += 1
        title, author = get_content(url)
        print(title)
        print(author)

