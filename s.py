# -*= coding:utf-8 -*-
from selenium import webdriver
import json
import time
import re
from selenium.webdriver.common.action_chains import ActionChains


class Taobao_spider():

    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml?redirectURL=http://s.taobao.com/search'
        self.f = open('1.txt', 'a', encoding='utf-8')
        self.f_1 = open('taobao.txt', 'a', encoding='utf-8')
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.maximize_window()
        self.page_num = 1
        time.sleep(10)
        input_ele = self.driver.find_element_by_xpath('//*[@id="q"]')
        input_ele.send_keys('T恤')
        submit_btn = self.driver.find_elements_by_class_name('icon-btn-search')[0]
        submit_btn.click()

    def get_firstpage_good_list(self):
        goods_list = self.driver.find_elements_by_xpath("//img[@class='J_ItemPic img']")
        return goods_list

    def get_goods_list(self):
        # try:
        if self.page_num == 1:
            index = 0
        else:
            index = 1
        next_page_btn = self.driver.find_elements_by_class_name("J_Pager")[index]
        action = ActionChains(self.driver)
        action.move_to_element(next_page_btn).perform()
        self.driver.execute_script('window.scrollTo(0, 0)')
        print('等待页面跳转')
        for i in range(1):
            print(i)
            time.sleep(1)
        next_page_btn = self.driver.find_elements_by_class_name("J_Pager")[index]
        next_page_btn.click()
        goods_list = self.driver.find_elements_by_xpath("//img[@class='J_ItemPic img']")
        self.page_num += 1
        return goods_list
        # except:
        #     self.driver.refresh()
        #     print('刷新页面')
        #     return self.get_goods_list()

    def get_detail_page(self, goods_list):
        # try:
        for goods in range(goods_list[:20].__len__()):
            time.sleep(1)
            self.driver.find_elements_by_xpath("//img[@class='J_ItemPic img']")[goods].click()
            handles = self.driver.window_handles
            for i in handles:
                if i != self.driver.current_window_handle:
                    print('切换窗口')
                    self.driver.switch_to_window(i)
                    text = self.driver.page_source
                    self.parse_page(text)
                    break
            self.driver.close()
            self.driver.switch_to_window(handles[0])
        # except:
        #     self.get_detail_page(goods_list)

    def taobao_goods_parse(self, text):
        li_ele_list = self.driver.find_elements_by_xpath("//ul[@class='J_TSaleProp tb-clearfix']//li")
        span_ele_list = self.driver.find_elements_by_xpath("//ul[@class='J_TSaleProp tb-clearfix']//span")
        dict_chima = dict()
        print('提取尺码')
        if li_ele_list.__len__() != span_ele_list.__len__():
            return 0
        for i in range(li_ele_list.__len__()):
            dict_chima[li_ele_list[i].text] = span_ele_list[i].text
        str_chima = json.dumps(dict_chima)
        print(str_chima)
        print('1')
        text = re.search(r"valItemInfo      : (\{[^)]*)", text, re.S)
        print('2')
        json_text = json.dumps(text.group(1)[:-1])
        print('3')
        content = json_text[:-1] + str_chima + '}'
        print(content)
        print(content, file=self.f_1)
        print('结束')

    def parse_page(self, text):
        # try:
        text = re.search(r"TShop.Setup\(([^\<]*)", text, re.S)
        text = text.group(1)[:-6].strip()[:-2].strip()
        dict_new = json.loads(text)
        action = ActionChains(self.driver)
        btn_ele = self.driver.find_element_by_partial_link_text('立即购买')
        action.move_to_element(btn_ele).perform()
        for key_demo in dict_new["propertyPics"].keys():
            print(key_demo)
            if key_demo != "default":
                key = key_demo.strip(';')
                xpath_str = '//li[@data-value="%s"]/a' % key
                btn = self.driver.find_element_by_xpath(xpath_str)
                try:
                    action.move_to_element(btn_ele).perform()
                    btn.click()
                    discount_price = self.driver.find_element_by_xpath(
                        '//div[@class="tm-promo-price"]/span[1]').text
                    dict_new["propertyPics"][key_demo].append({'discount_price':discount_price})
                    print(discount_price)
                except:
                    dict_new["propertyPics"][key_demo].append({'discount_price': ''})
        text = json.dumps(dict_new)
        print(text, file=self.f)
        # except:
        #     pass
            # self.taobao_goods_parse(self.driver.page_source)

    def run(self, num):
        #num 为页数
        first_goods_list = self.get_firstpage_good_list()
        self.get_detail_page(goods_list=first_goods_list)
        print('第1页爬取成功')
        k = 1
        for i in range(num-1):
            k += 1
            goods_list = self.get_goods_list()
            self.get_detail_page(goods_list=goods_list)
            print('第%s页爬取成功' % k)
        self.f.close()
        print('爬取结束')
tao_spider = Taobao_spider()
tao_spider.run(5)


