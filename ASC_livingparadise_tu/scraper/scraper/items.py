# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from apps.paradise.models import NvProduct, Product


class ScraperItem(DjangoItem):
    django_model = Product
