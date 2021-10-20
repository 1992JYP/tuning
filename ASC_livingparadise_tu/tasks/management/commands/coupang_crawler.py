from django_task.task_command import TaskCommand


class Command(TaskCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        print("======== coupang crawler ============")
        parser.add_argument('key_word', type=int)

    def handle(self, *args, **options):
        from tasks.models import coupangcrawlerTask
        self.run_task(coupangcrawlerTask, **options)
