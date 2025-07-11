# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter


class FmPipeline:
    def process_item(self, item, spider):
        pass
        # _type = item.get("type")
        # if _type=="img":
        #     try:
        #         os.mkdir('images')
        #     except:
        #         pass
        #     file_name = os.path.join('images', item.get("img_name"))
        #     with open(file_name, 'wb') as f:
        #         f.write(item.get("img_bytes"))
        #     print("---img---")
        # elif _type=="info":
        #     print("---info---")
