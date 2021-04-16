import sys
import functools
from queue import Queue
from types import GeneratorType
from typing import List, Union, Dict, Any, Generator
from multidict import MultiDict

from commandintegrator.tools.schedule.components import TimeTrigger, Job

"""
Details:
    2020-07-05
    
    commandintegrator framework source file with decorator
    objects

    This module contains functions and classes that are
    intended for use as decorators throughout the stack.
"""


# noinspection PyPep8Naming
class schedule:
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
    def schedule_default_catcher(job: Job) -> None:
        """
        This is the default method for return values of
        scheduled jobs, if no recipient is specified
        by the creator of a scheduled job.

        All Jobs without a designated recipient
        callable will have their return value end
        up in this method which maps their return
        value with themselves as source, in a dict object
        and stored in the public accessible queue "outputs".

        :param job: Job instance which has been executed
                    at least once
        """
        schedule.outputs.put(job)

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

        """
        Evaluates whether the Job should pass itself to
        the recipient, or not. Used when no recipient
        is provided, and schedule.queue is the final
        destination for the Job. It is useful information
        in the Job instance itself here, so it makes sense
        that in this queue the job itself resides with its
        return value cached in its return_value field.
        """
        return_self = False

        # Configure a TimeTrigger based on provided rules
        trigger = TimeTrigger(every=kwargs.get("every"),
                              at=kwargs.get("at"),
                              after=kwargs.get("after"))

        # Extract any kwargs to be passed to the scheduled callable
        if not (func_kwargs := kwargs.get("kwargs")):
            func_kwargs = {}

        # Set schedule_default_catcher as default recipient
        # if not specified
        if not (recipient := kwargs.get("recipient")):
            recipient = schedule.schedule_default_catcher
            return_self = True

        # Create a Job instance, start it and add it to dicts
        job = Job(func=func, trigger=trigger,
                  recipient=recipient, return_self=return_self,
                  **func_kwargs)
        job.start()

        schedule.name_job_map.add(job.name, job)
        schedule.id_job_map[job.native_id] = job

    @staticmethod
    def method(**kwargs):
        """
        Decorator function for self.run, used as
        @Schedule.method(**kwargs) (See TimeTrigger class
        for these kwargs)
        """
        def decorator(func):
            schedule.run(func, **kwargs)
        return decorator

    @staticmethod
    def get_jobs(job_name: str = None, job_id: int = None) -> Generator[Job, Any, None]:
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
                for job in schedule.name_job_map.getall(job_name):
                    yield job
            except KeyError:
                yield
        elif job_id:
            try:
                yield schedule.id_job_map[int(job_id)]
            except KeyError:
                yield

    @staticmethod
    def kill_job_gracefully(job_name=None, job_id=None, job_kwargs=None):
        """
        Kill jobs gracefully.
        :param job_name: str, name of the job
        :param job_id: int, id of the job
        :param job_kwargs: kwargs for the job, to
                separate jobs from others of the same
                function but with unique kwargs
        """
        for job in schedule.get_jobs(job_name, job_id):
            if job_kwargs and job.kwargs == job_kwargs:
                job.kill_gracefully()
                print(f"Found job for kill: {job}")
            elif not job_kwargs:
                print(f"Found job for kill: {job}")
                job.kill_gracefully()

    @staticmethod
    def get_all_jobs() -> Generator[Job, Any, None]:
        """
        Returns all jobs, in name_job_map and id_job_map
        combined.
        :rtype: Job
        """
        for i in schedule.id_job_map.values():
            yield i


class Logger:
    """
    Wrapper class designed to work as a method
    decorator, making logging of output and caught
    errors easier.

    Begin with creating the logging instance of
    choice, configuring it the way you want, then
    pass it to the logger.set_logger method.

    __verify_complete (method):
        Internal use only. Used upon importing the package
        in __init__.py, to ensure the Logger class has a 
        dedicated `logger` instance to work with.

    loggedmethod (decorator method):
        This method is designed to be a decorator for bound
        and unbound methods in a software stack. The log method
        is static and has a closure method called inner, where
        the wrapped method is executed. Exceptions & return from
        the wrapped method are both logged to the log file using
        the static 'logging' instance, configured for the class.
        Simply add the decorator above your method to enable logging
        for it. Presuming you import this package as commandintegrator;

        @commandintegrator.logger.log
        def myfunc(self, *args, **kwargs):
            ...

    log (method):
        If you want to manually log custom messages in your code,
        you can call this method. See method docstring / help
        for parameters and how to use it.
    """

    LOG_INSTANCE = None

    @staticmethod
    def __verify_config_complete():
        if Logger.LOG_INSTANCE is None:
            sys.stderr.write('commandintegrator -- logging error: '
                             'Cannot log, no log set.\r\n')
            sys.stderr.write('Configure an instance of logger, and'
                             ' pass it to Logger.set_logger()\r\n.')

    @staticmethod
    def loggedmethod(func):
        """
        Wrapper method for providing logging functionality.
        Use @logger to implement this method where logging
        of methods are desired.
        :param func:
            method that will be wrapped
        :returns:
            function
        """
        @functools.wraps(func)
        def inner(*args, **kwargs):
            """
            Inner method, executing the func paramter function,
            as well as executing the logger.
            :returns:
                Output from executed function in parameter func
            """
            try:
                results = func(*args, **kwargs)
                Logger.LOG_INSTANCE.debug(
                    f'Ran method "{func.__name__}" in {func.__module__} '
                    f'with ARGS: {args} & KWARGS: {kwargs} & RETURN: {results}')
                return results
            except Exception as e:
                Logger.LOG_INSTANCE.error(
                    f'Exception occured in {func.__name__}: {e}')
                raise e
        return inner

    @staticmethod
    def log(message: str, level="debug") -> None:
        """
        Allow for manual logging during runtime.
        :param message: str, message to be logged
        :param level: level for logging
        :returns:
            arbitrary
        """
        log_levels = {'info': lambda _message: Logger.LOG_INSTANCE.info(_message),
                      'debug': lambda _message: Logger.LOG_INSTANCE.debug(_message),
                      'error': lambda _message: Logger.LOG_INSTANCE.error(_message)}
        try:
            log_levels[level](message)
        except KeyError:
            log_levels['debug'](message)

    @staticmethod
    def set_logger(logging):
        Logger.LOG_INSTANCE = logging


# Deprecated since 1.3.1
def scheduledmethod(func):
    """
    Schedule method decorator. In certain applications
    the ability to automatically call functions by the
    means of a schedule in some manner, for example with
    a schedule.Scheduler() instance object, it can be 
    desired to direct messages to different channels in 
    the front end application such as a Discord or Slack
    server. If, however the method is called as per usual,
    the behavior is not altered. Add this decorator above
    a method in your stack, and then add the parameter 
    'channel' when you call it through the scheduler routine.

    The returned value from this will be a dictionary where
    the function output is under the 'result' key, and the
    channel is under the 'channel' key, as seen below.
    """

    # Deprecated since 1.3.1
    raise DeprecationWarning("The scheduledmethod decorator is deprecated "
                             "since 1.3.1 and is no longer supported. "
                             "But fear not - Check out the 'schedule.method' "
                             "decorator to use the built-in scheduler in the "
                             "framework!")

    # noinspection PyUnreachableCode
    @functools.wraps(func)
    def scheduled_method_wrapper(*args, **kwargs):
        try:
            channel = kwargs['channel']
        except KeyError:
            return func(*args, **kwargs)
        else:
            kwargs.pop('channel')
            return {
                'result': func(*args, **kwargs),
                'channel': channel
            }

    return scheduled_method_wrapper
