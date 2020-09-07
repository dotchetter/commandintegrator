import sys
import os
import json
import itertools
import logging
from datetime import datetime
from pathlib import Path

from .tools.apihandles import RestApiHandle
from .tools.pollcache import PollCache
from .baseclasses.baseclasses import FeatureBase, FeatureCommandParserBase
from .core.commandprocessor import CommandProcessor
from .core.interpretation import Interpretation
from .core.decorators import Logger as logger
from .core.decorators import scheduledmethod
from .core.pronounlookuptable import PronounLookupTable
from .core.enumerators import CommandPronoun
from .core.internals import _cim, is_dst
from .core.callback import Callback

from .models.commandparser import CommandParser
from .models.feature import Feature
from .models.message import Message

__version__ = '1.2.8'

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

LANGUAGE_FILE_DIR = CONFIG_FILE_DIR
LANGUAGE_FILE_NAME = Path('language.json')
LANGUAGE_FILE_FULLPATH = LANGUAGE_FILE_DIR / LANGUAGE_FILE_NAME

# Failsafe defaults
LOG_FILE_DIR = Path('.')
LOG_FILE_NAME = Path('commandintegrator.log')
LOG_FILE_FULLPATH = Path('.')
APPEND_LOGFILES = False
CHOSEN_LANGUAGE = "en-us"

# ---------------- Assert settings file presence --------------- # 

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
        CHOSEN_LANGUAGE = settings['chosen_language']
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

# ------------- Assert file precense and load language ------------ #
try:
    with open(LANGUAGE_FILE_FULLPATH, 'r', encoding = 'utf-8') as f:
        language_file = json.loads(f.read())
        pronoun_identifiers = language_file['pronoun_identifiers']
        CommandProcessor.DEFAULT_RESPONSES = language_file['default_responses']
        PronounLookupTable.assign_pronoun_identifiers(pronoun_identifiers, CHOSEN_LANGUAGE)
except Exception as e:
    sys.stderr.write(f'{_cim.err}: Could not load pronouns for language: {CHOSEN_LANGUAGE}')
    sys.exit()