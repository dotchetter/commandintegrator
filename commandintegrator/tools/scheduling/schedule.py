import functools
from datetime import datetime
from queue import Queue
from typing import Dict, Generator, Any

from multidict import MultiDict
from commandintegrator.tools.components import Job, TimeTrigger


class Scheduled:
    """
    Namespacing static class to schedule
    function calls, using TimeTrigger and Job
    objects.

    Works as a decorator using the
    'method' method as @Schedule.method,
    or by calling Schedule.run() withr
    provided args.
    """
    id_job_map: Dict[int, Job] = {}
    name_job_map: MultiDict[str, Job] = MultiDict()
    outputs: Queue[Job] = Queue()

    @staticmethod
    def run(func, at: str=None, every: str=None,
            after: str=None, exactly_at: datetime=None,
            recipient: str=None) -> None:
        """
        Registers a new Scheduled Job and starts
        the countdown for the Job.
        :param func: the callable to be called when
                     the TimeTrigger is triggered

        Evaluates whether the Job should pass itself to
        the recipient, or not. Used when no recipient
        is provided, and schedule.queue is the final
        destination for the Job. It is useful information
        in the Job instance itself here, so it makes sense
        that in this queue the job itself resides with its
        return value cached in its return_value field.

        :param func: partials object, ready wrapped function
                     bundled with its associated args and kwargs
                     and context
        :param at: str, argument for TimeTrigger object
        :param every: str, argument for TimeTrigger object
        :param after: str, argument for TimeTrigger object
        :param exactly_at: datetime, optional exact point in time
        :param recipient: callable, optional. Which function
                          to pass any return value from executed
                          job.
        """

        return_self = False

        # Configure a TimeTrigger based on provided rules
        trigger = TimeTrigger(every=every, at=at,
                              after=after, exactly_at=exactly_at)

        if not (recipient := recipient):
            recipient = Scheduled.schedule_default_catcher
            return_self = True

        job = Job(func=func,
                  trigger=trigger,
                  recipient=recipient,
                  return_self=return_self)
        job.start()
        print("Schedule started job") # TODO debug
        Scheduled.name_job_map.add(job.name, job)
        Scheduled.id_job_map[job.native_id] = job

    @staticmethod
    def schedule_default_catcher(job: Job) -> None:
        """
        This is the default method for return values of
        Scheduled jobs, if no recipient is specified
        by the creator of a Scheduled job.

        All Jobs without a designated recipient
        callable will have their return value end
        up in this method which maps their return
        value with themselves as source, in a dict object
        and stored in the public accessible queue "outputs".

        :param job: Job instance which has been executed
                    at least once
        """
        Scheduled.outputs.put(job)

    @staticmethod
    def get_jobs(job_name: str = None, job_id: int = None) -> \
            Generator[Job, Any, None]:
        """
        Returns Job instance(s) that matches provided
        args. Since many jobs can share the same name,
        multidict is used when mapping against its name.
        Their native_id is unique however, thus a regular
        dict is used for mapping jobs against their native_id.


        :param job_name: str, name of the job to return (optional)
        :param job_id: int, id of the job to return (optional
        :rtype: Job instance
        :raises: ValueError, if both name and id are None
        """
        if job_name is None and id is None:
            raise ValueError("either job_name or job_id must be specified")

        if job_name:
            try:
                for job in Scheduled.name_job_map.getall(job_name):
                    yield job
            except KeyError:
                yield
        elif job_id:
            try:
                yield Scheduled.id_job_map[int(job_id)]
            except KeyError:
                yield

    @staticmethod
    def kill_job_gracefully(job_name=None, job_id=None):
        """
        Kill jobs gracefully.
        :param job_name: str, name of the job
        :param job_id: int, id of the job
        """
        for job in Scheduled.get_jobs(job_name, job_id):
            job.kill_gracefully()

    @staticmethod
    def get_all_jobs() -> Generator[Job, Any, None]:
        """
        Returns all jobs, in name_job_map and id_job_map
        combined.
        :rtype: Job
        """
        for i in Scheduled.id_job_map.values():
            yield i

    @staticmethod
    def has_outputs() -> bool:
        """
        Returns whether there are outputs in
        the output queue 'Scheduled.outputs'
        """
        return bool(Scheduled.outputs.qsize())


class Decorate:

    def __init__(self, **decorator_kwargs):

        self.scheduling_configured = False

        if job_kwargs := decorator_kwargs.get("kwargs"):
            self.timetrigger_kwargs = decorator_kwargs.pop("kwargs")
        else:
            job_kwargs = {}
        self.job_kwargs = job_kwargs
        self.timetrigger_kwargs = decorator_kwargs


        print(f"DEBUG: Decorate.__init__: self.timetrigger_kwargs: {self.timetrigger_kwargs}")
        print(f"DEBUG: Decorate.__init__: self.job_kwargs: {self.job_kwargs}")

    def __call__(self, func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):

            return_value = func(*args, **self.job_kwargs)
            if not self.scheduling_configured:

                job_func = lambda: func(*args, **self.job_kwargs)

                Scheduled.run(job_func, **self.timetrigger_kwargs)
                self.scheduling_configured = True
            return return_value
        return decorated

    def __get__(self, ctx, owner):
        return functools.partial(self, ctx)