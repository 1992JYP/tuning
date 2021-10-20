from django.contrib import admin
from django_task.admin import TaskAdmin

from .models import ScraperTask, CountBeansTask, CountBeansTaskThreaded, SendEmailTask, navercrawlerTask , coupangcrawlerTask , gpcrawlerTask

@admin.register(ScraperTask)
class ScraperTaskAdmin(TaskAdmin):

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ['num_beans', ]


@admin.register(CountBeansTask)
class CountBeansTaskAdmin(TaskAdmin):

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ['num_beans', ]


@admin.register(CountBeansTaskThreaded)
class CountBeansTaskThreadedAdmin(TaskAdmin):

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ['num_beans', ]


@admin.register(SendEmailTask)
class SendEmailTaskAdmin(TaskAdmin):

    pass

@admin.register(navercrawlerTask)
class navercrawlerTaskAdmin(TaskAdmin):
    pass

@admin.register(coupangcrawlerTask)
class couapngcrawlerTaskAdmin(TaskAdmin):
    pass

