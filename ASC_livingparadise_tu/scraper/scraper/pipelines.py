# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScraperPipeline(object):
    """
    Saves Item to the database
    """
    def process_item(self, item, spider):
        print("++++++++++++++++ called scrapper pipeline ++++++++++++++++++")
        item.save()
        return item

"""
class PropertyStatusPipeline(object):

    Replace text for item status i.e For Rent will be replaced with Rent.

    def process_item(self, item, spider):
        if item.get('status'):
            item['status'] = item['status'].replace('For ', '')
            return item


class PropertyPricePipeline(object):

    Removes signs from the price value. i.e replaces 10000/= with 10000

    def process_item(self, item, spider):
        if item.get('price'):
            item['price'] = item['price'].replace('/=', '')
            return item


# useful for handling different item types with a single interface
from word2number import w2n

class ConvertNumPipeline(object):

    Converts words to number values for bedrooms and bathrooms

    def process_item(self, item, spider):
        if item.get('bathrooms'):
            item['bathrooms'] = w2n.word_to_num(item['bathrooms'])
        if item.get('bedrooms'):
            item['bedrooms'] = w2n.word_to_num(item['bedrooms'])
        return item
"""
