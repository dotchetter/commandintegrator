import time
from queue import Queue
from typing import Callable
from datetime import datetime, timedelta
from threading import Thread

from commandintegrator.schedule.scheduled import Scheduled


class TimeTrigger:
    """
    TimeTrigger class

    The TimeTrigger class acts like a timed clock
    which can be wound up using different measurements
    and units of time. It can be set to trigger
    at a certain time, after a certain amount of time
    has passed, be a recurring trigger with a defined
    interval of delay.

    """
    timeformat = "%H:%M:%S"
    day_int = {
        "day": (0, 1, 2, 3, 4, 5, 6),
        "monday": (0,),
        "tuesday": (1,),
        "wednesday": (2,),
        "thursday": (3,),
        "friday": (4,),
        "saturday": (5,),
        "sunday": (6,),
    }

    timeunits = {
        "hour": timedelta(hours=1),
        "minute": timedelta(minutes=1),
        "second": timedelta(seconds=1),
    }

    def __init__(self, at=None, every=None, after=None):
        """
        Configures the TimeTrigger object according
        to provided arguments.

        :param every: str, a day, every day or timeunit.
            Valid parameters:
                "day"
                "monday"
                "tuesday"
                "wednesday"
                "thursday"
                "friday"
                "saturday"
                "sunday"
                "hour"
                "minute"
                "second"
        param at: str, time of scheduling.
                  Valid in HH:MM:SS format or HH:MM format.
                  Example: "10:00" or "10:00:22". Seconds (SS)
                  defaults to 00 if not specified.
        """
        self.amount_of_runs = 0
        self.next_trigger: datetime = datetime.now()
        self.reoccurring: bool = False
        self.timedelta_interval: timedelta = None
        self.days_to_run: tuple[int] = None
        self.after = None

        if at:
            at = self.__validate_timestring(at)
            parsed_time = datetime.strptime(at, self.timeformat)
            self.next_trigger = self.next_trigger.replace(
                hour=parsed_time.hour,
                minute=parsed_time.minute,
                second=parsed_time.second)
        elif after:
            after = self.__validate_timestring(after)
            parsed_time = datetime.strptime(after, self.timeformat)
            self.after = timedelta(hours=parsed_time.hour,
                                   minutes=parsed_time.minute,
                                   seconds=parsed_time.second)
        if every:
            self.reoccurring = True
            if not (_repeat_every := self.day_int.get(every)):
                if not (_repeat_every := self.timeunits.get(every)):
                    raise ValueError(
                        f"'{every}' is an invalid value for 'every'")
            if isinstance(_repeat_every, tuple):
                # It's a day of week, or every day in the week
                self.days_to_run = _repeat_every
            elif isinstance(_repeat_every, timedelta):
                # It's every minute, hour or second
                self.timedelta_interval = _repeat_every
        if not any((at, every, after)):
            raise AttributeError("TimeTrigger needs at least one rule "
                                 "for scheduling: 'every', 'at', 'after'")
        self.reset()

    def __repr__(self):
        return f"TimeTrigger(next_trigger={self.next_trigger}, " \
               f"amount_of_runs={self.amount_of_runs}, " \
               f"reoccuring={self.reoccurring})"

    @staticmethod
    def __validate_timestring(timestr: str) -> str:
        if len(timestr.split(":")) < 3:
            return f"{timestr}:00"
        return timestr

    def __bool__(self):
        return self.poll()

    def poll(self):
        if datetime.now() >= self.next_trigger:
            if self.reoccurring:
                self.reset()
            self.amount_of_runs += 1
            return True
        return False

    def reset(self) -> None:
        """
        Reset itself to a future point in time,
        based on the rules provided at instantiation.

        If for example it is configured to run
        every day, the next day in line will
        be assigned to the datetime object in
        self.next_trigger.

        If a timedelta is the configured interval,
        the self.next_trigger will be mutated with
        this value.
        :returns: None
        """
        if self.days_to_run:
            if datetime.now() >= self.next_trigger:
                self.next_trigger += timedelta(days=1)
            while not self.next_trigger.weekday() in self.days_to_run:
                self.next_trigger += timedelta(days=1)
        elif self.timedelta_interval:
            self.next_trigger += self.timedelta_interval
        if self.after:
            self.next_trigger += self.after


class Job(Thread):
    """
    Threaded job, scheduled for a specific
    interval and / or time of execution.

    The Job class is runnable as a separate
    thread, thus leaving any function that it's
    calling non-blocking.
    """

    def __init__(self, func: Callable,
                 trigger: TimeTrigger,
                 recipient: Callable,
                 **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.func = func
        self.trigger = trigger
        self.recipient = recipient
        try:
            self.name = func.__name__
        except AttributeError:
            raise SyntaxError("A method already decorated with "
                              "'@scheduled.method' cannot be scheduled "
                              "using scheduled.run")

    def __repr__(self):
        return f"Job(name={self.name}, " \
               f"is_alive={self.is_alive()}, " \
               f"recipient={self.recipient}, " \
               f"kwargs={self.kwargs}, " \
               f"trigger={self.trigger})"

    def run(self) -> None:
        """
        Thread overloaded method
        Await the TimeTrigger object to fire on
        it's point in time, and call the callable
        passed as self.func.
        """
        while True:
            if self.trigger:
                try:
                    self.recipient(self.func())
                except TypeError:
                    pass
            if not self.trigger.reoccurring and self.trigger.amount_of_runs > 0:
                break
            time.sleep(0.01)
        self.func = None
        self.trigger = None
