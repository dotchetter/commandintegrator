import models
from .pronounlookuptable import PronounLookupTable
from .decorators import Logger as logger
from .interpretation import Interpretation

class CommandProcessor:
    """
    This object, while integrated to a front end
    works as a way to parse and understand what a
    human is asking for. An object containing the 
    representation of the interpretation of said
    sentence or word is returned of class 
    Interpretation.
    """

    def __init__(self, pronoun_lookup_table: PronounLookupTable, default_responses: dict):
        self._pronoun_lookup_table = pronoun_lookup_table
        self._feature_pronoun_mapping = dict()
        self._default_responses = default_responses

    @property
    def features(self) -> tuple:
        return self._features
    
    @features.setter
    def features(self, features: tuple):
        if not isinstance(features, tuple):
            raise TypeError(f'{_cim.warn}: expected tuple, got {type(features)}')
        
        for feature in features:
            self._feature_pronoun_mapping[feature] = feature.mapped_pronouns
        self._features = features

    @logger
    def process(self, message: models.Message) -> Interpretation:
        """
        Part of the public interface. This method takes a models.Message
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
   
    def _interpret(self, message: models.Message) -> Interpretation:
        """
        Identify the pronouns in the given message. Try to 
        match the pronouns aganst the mapped pronouns property
        for each featrure. If multiple features match the set of
        pronouns, the message is given to each feature for keyword
        matching. The feature that returns a match is given the
        message for further processing and ultimately returning
        the response.
        """
        mapped_features = list()
        return_callable = None
        found_pronouns = self._pronoun_lookup_table.lookup(message.content)
        
        for feature in self._features:
            if bool(set(self._feature_pronoun_mapping[feature]).intersection(found_pronouns)):                
                if feature.command_parser.is_contender_for_processing(message): 
                    mapped_features.append(feature)

        if not mapped_features:
            return Interpretation(
                command_pronouns = found_pronouns,
                feature_name = None,
                original_message = tuple(message.content),
                response = lambda: random.choice(self._default_responses['NoResponse']))

        for feature in mapped_features:
            try:
                return_callable = feature(message)
            except NotImplementedError as e:
                return Interpretation(
                    command_pronouns = found_pronouns,
                    feature_name = feature.__class__.__name__,
                    response = lambda: random.choice(self._default_responses['NoImplementation']),
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
            response = lambda: random.choice(self._default_responses['NoSubCategory']),
            original_message = tuple(message.content))