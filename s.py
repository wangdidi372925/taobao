# -*= coding:utf-8 -*-
url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http://s.taobao.com/search'
from selenium import webdriver
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()
import time
time.sleep(10)
input_ele = driver.find_element_by_xpath('//*[@id="q"]')
input_ele.send_keys('T恤')
submit_btn = driver.find_elements_by_class_name('icon-btn-search')[0]
submit_btn.click()
# input_ele = driver.find_elements_by_class_name('search-combobox-input')[1]
# try:
#     input_ele.send_keys('T恤')
# except:
#     pass
# submit_btn = driver.find_elements_by_class_name('btn-search')[1]
# try:
#     submit_btn.click()
# except:
#     pass

goods_list = driver.find_elements_by_xpath("//img[@class='J_ItemPic img']")

import re
import json
# f = open('1.json', 'a')
# def parse_page(text):
#     text = re.search(r"TShop.Setup\((.*)[^<]", text, re.S)
#     text = text.group(1)[:-6].strip()[:-2].strip()
#     json.dump(text, f)
f = open('1.txt', 'a', encoding='utf-8')
def parse_page(text):
    text = re.search(r"TShop.Setup\(([^\<]*)", text, re.S)
    text = text.group(1)[:-6].strip()[:-2].strip()
    print(text)
    # json.dump('\n'+ text, f)
    print(text,file=f)

for goods in goods_list:
    time.sleep(2)
    goods.click()
    handles = driver.window_handles
    for i in handles:
        if i != driver.current_window_handle:
            print('切换窗口')
            driver.switch_to_window(i)
            print(driver.page_source)
            # script_ele =   driver.find_element_by_xpath('//*[@id="J_DetailMeta"]/div[1]/script[3]').text
            # print('标签是',script_ele)
            text = driver.page_source
            print(text)
            parse_page(text)

            break
    driver.close()
    driver.switch_to_window(handles[0])
f.close()



