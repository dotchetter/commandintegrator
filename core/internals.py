import pytz
from datetime import datetime
from dataclasses import dataclass

"""
Details:
    2020-07-05
    
    CommandIntegrator framework internal source file

Module details:
    
    data containers and functions used by objects in
    the CommandIntegrator package.
"""


def is_dst(dt: datetime = datetime.now(), timezone: str = "Europe/Stockholm"):
    """
    Method for returning a bool whether or not a timezone
    currently is in daylight savings time, useful for servers
    that run systems outside of the user timezone.
    :param dt:
        datetime object, default is .now()
    :param timezone:
        string, timezone to give pytz for the dst query.
        look up available timezones at this url:
        https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    :returns:
        bool
    """
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst = None)
    return timezone_aware_date.tzinfo._dst.seconds != 0

@dataclass
class _cim:
    """
    This class is only used as a namespace
    for internal messages used by exceptions
    or elsewhere by CommandIntegrator classes
    and functions. Not for instantiating.
    """
    deprecated_warn: str = "CommandIntegrator DEPRECATED WARNING"
    warn: str = "CommandIntegrator WARNING"
    err: str = "CommandIntegrator ERROR"