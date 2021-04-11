import time
from datetime import datetime
from queue import Queue

from commandintegrator.schedule.components import TimeTrigger, Job


class Scheduled:
    """
    Static class to schedule function
    calls, using TimeTrigger and Job
    objects.

    Works as a decorator using the
    'method' method as @Scheduled.method,
    or by calling Scheduled.run() with
    provided args.
    """
    jobs = Queue()
    outputs = Queue()

    @staticmethod
    def run(func, **kwargs):
        """
        Registers a new scheduled Job and starts
        the countdown for the Job.
        :param func: the callable to be called when
                     the TimeTrigger is triggered
        :param kwargs: kwargs passed to the callable
                       at time of call
        """
        trigger = TimeTrigger(every=kwargs.get("every"),
                              at=kwargs.get("at"),
                              after=kwargs.get("after"))

        if not (func_kwargs := kwargs.get("kwargs")):
            func_kwargs = {}
        if not (output := kwargs.get("output_destination")):
            output = Scheduled.outputs
        job = Job(func=func, trigger=trigger,
                  output=output, **func_kwargs)
        job.start()

    @staticmethod
    def method(**kwargs):
        """
        Decorator function for self.run, used as
        @Scheduled.method
        def foo():
            return bar

        :param kwargs: kwargs passed to the wrapped
                       function
        """
        def schedule_wrapper(func):
            Scheduled.run(func, **kwargs)
        return schedule_wrapper


if __name__ == "__main__":

    @Scheduled.method(at="23:02", every="tuesday", kwargs={"what": "Foo"})
    def five_seconds(what: str):
        return f"I say {what}!"

    @Scheduled.method(every="minute")
    def ten_seconds():
        return datetime.now().strftime("%H:%M:%S")

    while 1:
        time.sleep(0.01)
