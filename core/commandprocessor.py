import sys
import random
import traceback

from collections.abc import Iterable

from .internals import _cim
from .interpretation import Interpretation
from .pronounlookuptable import PronounLookupTable

from ..models.message import Message
from ..baseclasses.baseclasses import FeatureBase

"""
Details:
    2020-07-05
    
    CommandIntegrator framework ComandProcessor source file

Module details:
    
    The CommandProcessor is the routing object of
    CommandIntegrator, acting as the main agent that
    will direct messages to Features in the application.
"""

class CommandProcessor:
    """
    This object, while integrated to a front end
    works as a way to parse and understand what a
    human is asking for. An object containing the 
    representation of the interpretation of said
    sentence or word is returned of class 
    Interpretation. 

    Default Responses class variable is designed to be
    set by __init__ in this package, loaded from the
    local .json file. 
    """

    DEFAULT_RESPONSES: dict = None

    def __init__(self, default_responses: dict = None, pronoun_lookup_table: PronounLookupTable = None):
        if pronoun_lookup_table:
            message = f'{_cim.deprecated_warn}: ' \
                       'The "pronoun_lookup_table" property is no longer necessary.'
            sys.stdout.write(message)
        if default_responses:
            message = f'{_cim.deprecated_warn}: ' \
                       'The "default_responses" property is no longer necessary.'
            sys.stdout.write(message)

        self._feature_pronoun_mapping = dict()

        if CommandProcessor.DEFAULT_RESPONSES is None:
            sys.stderr.write(f'{_cim.err}: CommandProcessor has no default responses, exiting.')
            sys.exit()

    @property
    def features(self) -> tuple:
        return self._features
    
    @features.setter
    def features(self, features: tuple):
        if not isinstance(features, Iterable) and isinstance(features, FeatureBase):
            features = (features,)

        for feature in features:
            if isinstance(feature, FeatureBase):
                if feature.mapped_pronouns:
                    self._feature_pronoun_mapping[feature] = feature.mapped_pronouns
            else:
                raise AttributeError(
                    f'{_cim.err}: CommandProcessor does not accept provided features')
        self._features = features

    def process(self, message: Message) -> Interpretation:
        """
        Part of the public interface. This method takes a Message
        object (OR another construct with a .content property that is the message body)
        - and splits the .content property on space characters
        turning it in to a list. The message is decomposed by the
        private _interpret method for identifying pronouns, which
        funnel the message to the appropriate features in the 
        self._features collection. As an instance of Interpretation
        is returned from this call, it is passed on to the caller.
        """
        message.content = message.content.lower().split(' ')
        try:
            return self._interpret(message)
        except Exception as e:
            sys.stderr.write(f'{_cim.err} :Error occured in CommandProcessor _interpret function: {e}')
            return Interpretation(error = traceback.format_exc(),
                        response = lambda: f'CommandProcessor: Internal error, see logs.',
                        original_message = tuple(message.content))
   
    def _interpret(self, message: Message) -> Interpretation:
        """
        Identify the pronouns in the given message. Try to 
        match the pronouns aganst the mapped pronouns property
        for each featrure. If multiple features match the set of
        pronouns, the message is given to each feature for keyword
        matching. The feature that returns a match is given the
        message for further processing and ultimately returning
        the response.
        """
        return_callable = None
        found_pronouns = PronounLookupTable.lookup(message.content)
        mapped_features = [i for i in self._features if i.command_parser.is_contender_for_processing(message)]

        if not mapped_features:
            return Interpretation(
                command_pronouns = found_pronouns,
                feature_name = None,
                original_message = tuple(message.content),
                response = lambda: random.choice(CommandProcessor.DEFAULT_RESPONSES['NoResponse']))

        for feature in mapped_features:
            try:
                return_callable = feature(message)
            except NotImplementedError as e:
                return Interpretation(
                    command_pronouns = found_pronouns,
                    feature_name = feature.__class__.__name__,
                    response = lambda: random.choice(CommandProcessor.DEFAULT_RESPONSES['NoImplementation']),
                    original_message = tuple(message.content),
                    error = e)
            else:
                if return_callable is None:
                    continue
                return Interpretation(
                    command_pronouns = found_pronouns,
                    feature_name = feature.__class__.__name__,
                    response = return_callable,
                    original_message = tuple(message.content))

        return Interpretation(command_pronouns = found_pronouns,
            feature_name = feature.__class__.__name__,
            response = lambda: random.choice(CommandProcessor.DEFAULT_RESPONSES['NoCallbackBinding']),
            original_message = tuple(message.content))