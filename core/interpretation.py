from dataclasses import dataclass
from .enumerators import CommandPronoun

"""
Details:
    2020-07-05
    
    CommandIntegrator framework Interpretation source file

Module details:
    
    the Interpretation object represents the final
    output from a Feature after the processing is 
    done. It will be instantiated and attribute
    set by the CommandProcessor object, and contain
    data about the identified pronouns, name of the
    Feature instance that processed the message,
    definition and memory address (__repr__) of the
    method that was returned by the Feature (callback),
    any errors caught while executing the callback.
"""


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
