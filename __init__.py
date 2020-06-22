import sys
import os
import json
import itertools
import logging
import pytz
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from .apihandles import RestApiHandle
from .baseclasses import FeatureBase, FeatureCommandParserBase
from .commandprocessor import CommandProcessor
from .interpretation import Interpretation
from .pollcache import PollCache
from .decorators import Logger as logger
from .decorators import scheduledmethod
from .commandparser import CommandParser
from .pronounlookuptable import PronounLookupTable

VERSION = '1.2.5'

# ------- NOTES: COMMANDINTEGRATOR .SETTINGS FILE  ------- #
"""
The details below will read and configure CommandIntegrator
according to the settings found in the settings file, by default
named "commandintegrator.settings". 
The settings file is presumed to be located within the package
root. 

The configuration file is used throughout the framework, so editing
these values will require editing elsewhere in the stack where you
use the CommandProcessor class for instance, and assign default
response phrases.
"""

# - Edit these constants to your preference or leave default - #

# Default and recommended settings file configuration
CONFIG_FILE_DIR = Path(os.path.split(os.path.abspath(__file__))[0])
CONFIG_FILE_NAME = Path('commandintegrator.settings')
CONFIG_FILE_FULLPATH = CONFIG_FILE_DIR / CONFIG_FILE_NAME

# Failsafe defaults
LOG_FILE_DIR = Path('.')
LOG_FILE_NAME = Path('runtime.log')
LOG_FILE_FULLPATH = Path('.')
APPEND_LOGFILES = False

# -------------------- Assert file presence -------------------- # 

if not os.path.isfile(CONFIG_FILE_FULLPATH):
    _msg = f'CommandIntegrator: Could not find config file ' \
           f'{CONFIG_FILE_NAME} in {CONFIG_FILE_DIR}'
    sys.stderr.write(_msg)

# --------- Configure according to the settings in file -------- #

try: 
    with open(CONFIG_FILE_FULLPATH, 'r', encoding = 'utf-8') as f:
        settings = json.loads(f.read())
        APPEND_LOGFILES = settings['logfile_append']
        LOG_FILE_DIR = Path(settings['log_dir'])
        LOG_FILE_NAME = Path(settings['log_filename'])
except Exception :
    sys.stderr.write(f'{_cim.warn}: Could not access settings file, proceeding with defaults')

if not os.path.isdir(LOG_FILE_DIR):
    os.mkdir(LOG_FILE_DIR)

LOG_FILE_FULLPATH = LOG_FILE_DIR / LOG_FILE_NAME

# ----------------- Set up logging preferences ------------------ # 

append_switch = {True: 'a+', False: 'w'}

handler = logging.FileHandler(filename = LOG_FILE_FULLPATH, 
                              encoding = 'utf-8', 
                              mode = append_switch[APPEND_LOGFILES])

handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

log = logging.getLogger('CI Logger')
log.setLevel(logging.DEBUG)
log.addHandler(handler)
logger.set_logger(log)
logger.log(f'-- NEW LOGGING SESSION STARTED. DATETIME: {datetime.now()} -- ')

"""
I love you

- That was written by my girlfriend without me knowing about it, 
on that very line. I left my computer unlocked some time during 
a weekend. It's so sweet that I can't remove it, so it's here, 
a part of the framework forever, that's the way it is. Consider 
yourself the founder of an easteregg.

// Simon Olofsson, lead developer and founder of CommandIntegrator

"""

# --- Methods and classes used internally by CommandIntegrator ---- #
 
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
    warn: str = "CommandIntegrator WARNING"
    err: str = "CommandIntegrator ERROR"