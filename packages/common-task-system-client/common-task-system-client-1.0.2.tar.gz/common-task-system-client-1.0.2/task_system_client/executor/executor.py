
class BaseExecutor(object):
    category = None
    name = None

    def __init__(self, schedule):
        self.schedule = schedule
        self.task = schedule.task

    def run(self):
        raise NotImplementedError

    def on_success(self):
        pass

    def on_error(self, error):
        pass
