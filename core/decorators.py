import sys
import functools
import logging


"""
Details:
    2020-07-05
    
    CommandIntegrator framework source file with decorator
    objects

    This module contains functions and classes that are
    intended for use as decorators throughout the stack.
"""

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
        for it. Presuming you import this package as CommandIntegrator;

        @CommandIntegrator.logger.log
        def myfunc(self, *args, **kwargs):
            ...

    log (method):
        If you want to manually log custom messages in your code,
        you can call this method. See method docstring / help
        for parameters and how to use it.
    """

    LOG_INSTANCE = None

    def __verify_config_complete(self):
        if Logger.LOG_INSTANCE == None:
            sys.stderr.write('CommandIntegrator -- logging error: Cannot log, no log set.\r\n')
            sys.stderr.write('Configure an instance of logger, and pass it to Logger.set_logger()\r\n.')
    
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
            :param *args:
                arbitrary parameters for the wrapped function
            :param **kwargs:
                arbitrary keyword parameters for the wrapped function
            :returns:
                Output from executed function in parameter func
            """
            try:
                results = func(*args, **kwargs)
                Logger.LOG_INSTANCE.debug(f'Ran method "{func.__name__}" in {func.__module__} ' \
                          f'with ARGS: {args} & KWARGS: {kwargs} & RETURN: {results}')
                return results
            except Exception as e:
                Logger.LOG_INSTANCE.error(f'Exception occured in {func.__name__}: {e}')
                raise e
        return inner

    @staticmethod
    def log(message: str, level = 'debug') -> None:
        """
        Allow for manual logging during runtime.
        :param message:
            str
            message to be logged
        :returns:
            arbitrary
        """
        _log_output = f'(!) Manual log entry: {message}'
        _log_levels = {'info': lambda _message: Logger.LOG_INSTANCE.info(_message),
                       'debug': lambda _message: Logger.LOG_INSTANCE.debug(_message),
                       'error': lambda _message: Logger.LOG_INSTANCE.error(_message)}
        try:
            _log_levels[level](_log_output)
        except KeyError:
            _log_levels['debug'](_log_output)

    @staticmethod
    def set_logger(logging):
        Logger.LOG_INSTANCE = logging

def scheduledmethod(func):
    """
    Scheduled method decorator. In certain applications
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