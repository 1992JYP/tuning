from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        try:
            from django_task.utils import revoke_pending_tasks
            revoke_pending_tasks()
        except Exception as e:
            print(e)

