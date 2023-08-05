import logging
import sched
import time
from threading import Thread, Lock

logger = logging.getLogger(__name__)


class Scheduler:
    def __call__(self, func, *args, **kwargs):
        logger.info(f'Scheduling method {func.__name__} every {self.interval} seconds')
        self.func = func
        self.run()
        return self

    def __init__(self, interval, *args, **kwargs):
        self.interval = interval
        self.func = None
        self.args = args
        self.kwargs = kwargs
        self.scheduler = sched.scheduler(time.time, time.sleep)
        logger.info(f'Setup Scheduler every {self.interval} seconds')

        self.last_id = None
        self.thread = None

    def periodic(self):
        self.last_id = self.scheduler.enter(self.interval, 1, self.periodic, ())
        self.func(*self.args, **self.kwargs)

    def local_run(self):
        self.periodic()
        self.scheduler.run()

    def run(self):
        self.thread = Thread(target=self.local_run, name=f'schedule-{self.func.__name__}')
        self.thread.daemon = True
        self.thread.start()

    def cancel(self):
        logger.info(f'Cancel Scheduler for {self.func.__name__}')
        self.scheduler.cancel(self.last_id)


def scheduled(interval):
    return Scheduler(interval)
