from django_task.task_command import TaskCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from scraper.scraper import settings as my_settings
from scraper.scraper.spiders.product_spider import ProductSpider


class Command(TaskCommand):
    help = 'Release spider'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        print("======== threaded normal ============")
        parser.add_argument('num_beans', type=int)


    def handle(self, *args, **options):
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(ProductSpider)
        process.start()
