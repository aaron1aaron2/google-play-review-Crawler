# -*- coding: utf-8 -*-
__author__ = "yen-nan ho"

import re
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from IPython import embed

class Worker:
    def __init__(self, data_dt):
        assert type(data_dt) == dict, "wrong data type! input data need to be string."

        self.url = data_dt['url']
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
        self.info_dt = data_dt


    def run(self):
        html = requests.get(self.url, headers = self.headers)
        if html.status_code == 200:
            print('main requests success!') 

        self.soup = BeautifulSoup(html.text, 'lxml')

        self.get_main_info()
        self.get_comment()
    
    def get_main_info(self):
        self.info_dt['type'] = self.soup.find("a", itemprop="genre").text

        recommend_ls = self.soup.find_all("div", class_="WsMG1c nnK0zc")
        self.info_dt['recommend_ls'] = [i.text for i in recommend_ls[:5]]

        self.info_dt['describe'] = self.soup.find("div", jsname="sngebd").text

        self.info_dt['comment_num'] = self.soup.find("span",class_="AYi5wd TBRnV").text.replace(',','')

    def _load_all_comment(self, browser):
        last_height = browser.execute_script("return document.body.scrollHeight")
        row = 0
        test = 0
        while True: 
            htmlstring = browser.page_source
            if htmlstring.find('顯示更多內容') == -1:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.1)
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    test+=1
                    if test < 10:
                        continue
                    else:
                        break
                else:
                    last_height = new_height
                    test = 0
                    row += 40
            else:
                element = browser.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span")
                browser.execute_script("arguments[0].click();", element)
            if (row%100)==0:
                reviews = browser.find_elements_by_xpath("//span[@jsname='bN97Pc']") # find xpath
                print("[{}] >> comment:{}/{}".format(os.getpid(), len(reviews), self.info_dt['comment_num']))

                if (len(reviews)%10) != 0:
                    break
                # if len(reviews) >=100:
                #     break
        browser.close()

        return htmlstring

    def get_comment(self):

        # setting options
        chrome_options = Options() 
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("user-agent={}".format(self.headers))

        # run driver
        browser = webdriver.Chrome('chromedriver.exe',
                                    chrome_options=chrome_options
                                    )

        browser.implicitly_wait(5) # 隱式等待 5 秒, https://selenium-python-zh.readthedocs.io/en/latest/waits.html#id3
        browser.get(self.url+"&showAllReviews=true")

        # set window_size
        window_size = browser.execute_script("""
            return [window.outerWidth - window.innerWidth + arguments[0],
            window.outerHeight - window.innerHeight + arguments[1]];
            """, 2000, 2000)
        browser.set_window_size(*window_size)

        # load & get all comment
        htmlstring = self._load_all_comment(browser)
        comment_soup = BeautifulSoup(htmlstring, 'lxml')

        # extract comment info
        comment_name_ls = comment_soup.find_all("span", class_="X43Kjb")
        comment_name_ls = [i.text for i in comment_name_ls if i.text!="DeNA HONG KONG LIMITED"]
        comment_ls = comment_soup.find_all("span", jsname="bN97Pc")
        comment_ls = [i.text for i in comment_ls]
        comment_ls_2 = comment_soup.find_all("span", jsname="fbQN7e")
        comment_ls_2 = [i.text for i in comment_ls_2]

        star_time_ls = comment_soup.find_all("span", class_="nt2C1d")
        star_ls = [i.div.div['aria-label'][4] for i in star_time_ls]

        time_ls = [i.next_sibling.text for i in star_time_ls]

        support_ls = comment_soup.find_all("div", class_="jUL89d y92BAb")
        support_ls = [i.text for i in support_ls]

        self.info_dt['comment'] =list(zip(comment_name_ls, star_ls, time_ls, support_ls, comment_ls, comment_ls_2))



def start_worker(target):
    spider = Worker(data_dt = target)
    spider.run()

    return spider.info_dt

if __name__ == "__main__":

    df = pd.read_csv('data/game_basic_list.csv')
    target = df.to_dict(orient='records')[0]

    spider = Worker(data_dt = target)
    spider.run()