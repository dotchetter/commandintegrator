from dataclasses import dataclass
from .enumerators import CommandPronoun

@dataclass
class Interpretation:
    """
    This object represents the output from the
    CommandProcessor class. 

    command_pronouns: A collection of pronouns
    identified in the message.

    feature_name: Name of the feature responsible
    and ultimately selected to provide a response.

    callback_binding: Name of the method that
    is bound to the subcategory for the feature.

    original_message: The original message in 
    a tuple, split by space.

    response: The callable object that was returned
    from the Feature.

    error: Any exception that was caught upon parsing
    the message. 
    """
    command_pronouns: tuple(CommandPronoun) = ()
    feature_name: str = None
    original_message: tuple = ()
    response: callable = None
    error: Exception = None

    def __repr__(self):
        return str(self.__dict__)
