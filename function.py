import os

basedir = os.path.abspath(os.path.dirname(__file__))

def check_file(url):
    filename = os.path.join(basedir,url[27:])
    if os.path.isfile(filename + '.html'):
        print(filename + '.html' + ' is existed, continue')
        return True
    return False

def check_filepath(url):
    filename = url[27:]
    filepath = basedir
    folders = filename.split('/')
    for i in range(len(folders) - 1):
        filepath = os.path.join(filepath, folders[i])
        if not os.path.isdir(filepath):
            os.mkdir(filepath)

def download_page(driver):
    content = driver.page_source
    url = driver.current_url
    check_filepath(url)
    filename = os.path.join(basedir, url[27:])
    content = change_path(driver,filename,content)
    with open(filename + '.html','w',encoding='utf-8') as f:
        f.write(content)

def download_image(driver,url):
    driver.get(url)
    check_filepath(url)
    filename = os.path.join(basedir, url[27:])
    with open(filename, 'wb') as file:
        file.write(driver.find_element_by_tag_name('img').screenshot_as_png)

def change_path(driver,filename,html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    ret = soup.find("section", attrs={'id':'main'})
    if ret:
        tags = ret.find_all("a")
        for tag in tags:
            if tag.has_attr('href') and tag['href'][:4] != 'http':
                if tag['href'][0] == '#':
                    tag['href'] = tag['href'].replace('#',"%23")
                    tag['href'] = basedir + '/problems/domain/0' + tag['href'] + '.html'
                else:
                    tag['href'] = basedir + tag['href'] + '.html'
            elif tag.has_attr('href') and tag['href'][:33] == 'https://judgegirl.csie.org/images':
                download_image(driver,tag['href'])
        tags = ret.find_all("img")
        for tag in tags:
            if tag.has_attr('src') and tag['src'][:7] == '/images':
                tag['src'] = basedir + tag['src']
        return str(ret)
    return str(soup)