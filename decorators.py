import sys
import logging


"""
Module details:
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
    """

    LOG_INSTANCE = None

    def __init__(self, func: callable):
        self.func = func

    def __verify_config_complete(self):
        if Logger.LOG_INSTANCE == None:
            sys.stderr.write('CommandIntegrator -- logging error: Cannot log, no log set.\r\n')
            sys.stderr.write('Configure an instance of logger, and pass it to Logger.set_logger()\r\n.')

    def __call__(self, *args, **kwargs):
        """
        Inner method, executing the func paramter function,
        as well as executing the logger.
        :param *args:
            arbitrary parameters for the wrapped function
        :param **kwargs:
            arbitrary keyword parameters for the wrapped function
        :returns:
            Arbitrary return from executed method
        """
        try:
            results = self.func(*args, **kwargs)
            Logger.LOG_INSTANCE.debug(f'Ran method "{self.func.__name__}" in {self.func.__module__} ' \
                      f'with ARGS: {args} & KWARGS: {kwargs} & RETURN: {results}')
            return results
        except Exception as e:
            Logger.LOG_INSTANCE.error(f'Exception occured in {self.func.__name__}: {e}')
            raise e
        return results

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
        _log_levels = {'info': lambda _message: Logger.LOG_INSTANCE.info(_message),
                       'debug': lambda _message: Logger.LOG_INSTANCE.debug(_message),
                       'error': lambda _message: Logger.LOG_INSTANCE.error(_message)}
        try:
            _log_levels[level](message)
        except KeyError:
            _log_levels['debug'](message)

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
    def _inner(*args, **kwargs):
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
    return _inner