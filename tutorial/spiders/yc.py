# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import PetDiseaseItem
import time

class YcSpider(scrapy.Spider):
    name = 'yc'
    allowed_domains = ['yc.cn']
    start_urls = ['http://yc.cn/']

    def start_requests(self):
        root_url = "http://www.yc.cn/disease/wiki-{0}.html"
        for i in range(234,620):
            url = root_url.format(i)
            print("病症详情", url)
            yield scrapy.Request(url, meta={'index': i}, callback=self.parse)
            pass

    def format_index_to_cat(self,index):
        if index >= 565:
            return 4
        elif index >= 546:
            return  3
        elif index >= 518:
            return 2
        elif index >= 405:
            return 1
        elif index >= 234:
            return 0
        else :
            return 5

    def parse(self, response):
        # 更具需要解析出所有的病例数据
        # print("没有回调数据吗", response.meta['index'])
        url_str = response.url
        index = response.meta['index']
        cat_id_i = self.format_index_to_cat(index)
        
        # print("当前类别",index,cat_id_i)

        name_node = response.xpath('//*[@id="t"]/text()').get()
        name_str = name_node
        # 科目
        genera_node = response.xpath('/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[1]/span[2]/text()').get()
        genera_str = genera_node
        # 症状
        symptom_node = response.xpath('/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[2]/span[2]/text()').get()
        symptom_str = symptom_node

        print(name_str, genera_str, symptom_str)


        desc_html = response.xpath('//div[@class="desc"]')

        node_list = desc_html.xpath('*')
        
        # 概述
        is_intr = False
        intr_str = ''
        
        # 发病原因
        is_reason = False
        reason_str = ''

        # 主要症状
        is_symptom = False
        symptom_str = ''

        # 诊断标准
        is_standard = False
        standard_str = ''

        # 治疗方法
        is_way = False
        way_str = ''

        #防治方法
        is_prevention = False
        prevention_str = ''

        for item in node_list:
            text_node = item.xpath('./text()').get()
            # print("解析出来的文字", text_node)
            text_str = text_node

            if text_str == '概述':
                # print("激活 is_intr")
                is_intr = True
                continue
                
            if text_str == '发病原因':
                is_intr = False
                is_reason = True
                continue
                
            if text_str == '主要症状':
                is_reason = False
                is_symptom = True
                continue
                
            if text_str == '诊断标准':
                is_symptom = False
                is_standard = True
                continue

            if text_str == '治疗方法':
                is_standard = False
                is_way = True
                continue

            if text_str == '防治方法':
                is_way = False
                is_prevention = True
                continue

            if is_intr == True:
                # print("拼接数据 is_intr")
                intr_str += text_str
            
            if is_reason == True:
                reason_str = reason_str + text_str + ": "
                continue

            if is_symptom == True:
                symptom_str += text_str
                continue
            
            if is_standard == True:
                standard_str += text_str
                continue

            if is_way == True:
                way_str = way_str + text_str + ": "
                continue
            
            if is_prevention == True:
                prevention_str += text_str
                continue
        
        # print("输出最终的结果",intr_str,reason_str,symptom_str,standard_str,way_str,prevention_str)
        field_item = PetDiseaseItem()
        field_item["cat_id_i"] = cat_id_i
        field_item["url_str"] = url_str
        field_item["intr_str"] = intr_str
        field_item["is_delete_i"] = 0
        field_item["genera_str"] = genera_str
        field_item["name_str"] = name_str
        field_item["prevention_str"] = prevention_str
        field_item["standard_str"] = standard_str
        field_item["symptom_str"] = symptom_str
        field_item["way_str"] = way_str
        field_item["add_time_date"] = time.time()
        field_item["reason_str"] = reason_str
        yield field_item