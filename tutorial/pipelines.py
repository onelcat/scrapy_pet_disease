# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

import pymysql
class MySQLPipeline(object):

    # 打开数据库
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME','pet')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '19920105')

        self.db_conn =pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.insert_db(item)
        # print("插入数据")
        return item

    #插入数据
    def insert_db(self, item):
    #         name_str = scrapy.Field()
    # cat_id_i = scrapy.Field()
    # intr_str = scrapy.Field()
    # reason_str = scrapy.Field()
    # symptom_str = scrapy.Field()
    # standard_str  = scrapy.Field()
    # way_str = scrapy.Field()
    # add_time_date =  scrapy.Field()
    # is_delete_i = scrapy.Field()
    # genera_str = scrapy.Field()
    # prevention_str = scrapy.Field()
        values = (
            item["name_str"],
            item["cat_id_i"],
            item["intr_str"],
            item["reason_str"],
            item["symptom_str"],
            item["standard_str"],
            item["way_str"],
            item["add_time_date"],
            item["is_delete_i"],
            item["genera_str"],
            item["prevention_str"],
            item["url_str"]
        )
        print("存储数据",self.db_conn)
        sql = 'insert into cshopmall_disease(name, cat_id, intr, reason, symptom, standard, way, add_time, is_delete, genera, c_prevention,c_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        self.db_cur.execute(sql, values)