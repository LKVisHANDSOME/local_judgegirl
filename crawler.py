import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from function import download_page, check_file

opts = Options()
opts.add_argument("--incognito")
proxy = "socks5://localhost:9050"
opts.add_argument('--proxy-server={}'.format(proxy))
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
opts.add_argument("user-agent={}".format(ua))
PATH = "C:/Users/a2320/Desktop/coding/python/chromedriver_win32/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(PATH)


basedir = os.path.abspath(os.path.dirname(__file__))

driver.get("https://judgegirl.csie.org/problems/domain/0")

time.sleep(2)

download_page(driver)

container = driver.find_element_by_id('container')

topics = container.find_elements_by_class_name('pure-menu-link')
topic_links = []
for topic in topics:
    if topic.text == 'Domain':
        continue
    topic_links.append(topic.get_attribute('href'))

for topic_link in topic_links:
    driver.get(topic_link)
    print(topic_link)
    driver.refresh()
    time.sleep(3)
    download_page(driver)
    problem_blocks = driver.find_elements_by_class_name('problem-item')
    problem_links = []
    for problem_block in problem_blocks:
        problem = problem_block.find_element_by_tag_name('a')
        problem_links.append(problem.get_attribute('href'))
    for problem_link in problem_links:
        number = problem_link[37:]
        if os.path.isfile(basedir+'/problem/0/'+str(number)+'.html'):
            print(basedir+'/problem/0/'+str(number)+'.html exist, continue')
            continue
        print(problem_link)
        driver.get(problem_link)
        time.sleep(3)
        download_page(driver)
        print('https://judgegirl.csie.org/testdata/download/' + str(number))
        driver.get('https://judgegirl.csie.org/testdata/download/' + str(number))
        time.sleep(2)
        download_page(driver)
        testcase_list = driver.find_element_by_class_name('pure-u-1')
        testcases = testcase_list.find_elements_by_class_name('pure-menu-link')
        testcase_links = []
        for testcase in testcases:
            testcase_links.append(testcase.get_attribute('href'))
        for testcase_link in testcase_links:
            if check_file(testcase_link):
                continue
            print(testcase_link)
            driver.get(testcase_link)
            download_page(driver)
            time.sleep(3)
        
        files = os.listdir('C:\\Users\\a2320\\Downloads')
        for file in files:
            if os.path.isfile(basedir+'/downloads/testdata/'+str(number)+'/'+file+'.html'):
                os.remove('C:\\Users\\a2320\\Downloads\\'+file)
            else:
                os.rename('C:\\Users\\a2320\\Downloads\\'+file,basedir+'/downloads/testdata/'+str(number)+'/'+file+'.html')
    time.sleep(2)

exit(1)