
# 수정 2021-07-12 이유인

from django.db import models
from django.conf import settings
# from django_task.models import TaskRQ
from django_task.models import TaskThreaded


################################################################################

class ScraperTask(TaskThreaded):

    num_beans = models.PositiveIntegerField(default=100)

    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import ScraperJob
        return ScraperJob


class CountBeansTask(TaskThreaded):

    num_beans = models.PositiveIntegerField(default=100)

    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import CountBeansJob
        return CountBeansJob


class CountBeansTaskThreaded(TaskThreaded):

    num_beans = models.PositiveIntegerField(default=100)

    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import CountBeansJob
        return CountBeansJob


class SendEmailTask(TaskThreaded):

    sender = models.CharField(max_length=256, null=False, blank=False)
    recipients = models.TextField(null=False, blank=False,
        help_text='put addresses in separate rows')
    subject = models.CharField(max_length=256, null=False, blank=False)
    message = models.TextField(null=False, blank=True)

    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import SendEmailJob
        return SendEmailJob

class navercrawlerTask(TaskThreaded):
    key_word = models.CharField(max_length=256, default='생활낙원')
    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import navercrawlerJob
        return navercrawlerJob


class coupangcrawlerTask(TaskThreaded):
    key_word = models.CharField(max_length=256, default='생활낙원')
    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import coupangcrawlerJob
        return coupangcrawlerJob




class gpcrawlerTask(TaskThreaded):   # 글로우픽 크롤러
    key_word = models.CharField(max_length=256, default='코스메카')
    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import gpcrawlerJob
        return gpcrawlerJob


class cpcrawlerTask(TaskThreaded):    # 코스메카 쿠팡크롤러
    key_word = models.CharField(max_length=256, default='코스메카')
    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import cpcrawlerJob
        return cpcrawlerJob


class nccrawlerTask(TaskThreaded):   # 코스메카네이버 크롤러
    key_word = models.CharField(max_length=256, default='코스메카')
    TASK_QUEUE = None
    #TASK_TIMEOUT = 10
    DEFAULT_VERBOSITY = 2
    LOG_TO_FIELD = True
    LOG_TO_FILE = False

    @staticmethod
    def get_jobclass():
        from .jobs import nccrawlerJob
        return nccrawlerJob



