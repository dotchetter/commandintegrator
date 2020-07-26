import random
import json
import traceback
import sys

from types import LambdaType
from ast import literal_eval
from pprint import pprint
from os import system
from datetime import datetime, timedelta, time
from enum import Enum, auto
from abc import ABC, abstractmethod

from ..core.callback import Callback
from ..core.internals import _cim
from ..core.enumerators import CommandPronoun
from ..models.message import Message

"""
Details:
    2020-06-21
    
    CommandIntegrator framework baseclass source file

Module details:
    
    This file contains abstract and base classes for 
    the framework called CommandIntegrator. 

    In order for a developer to integrate their software
    with a way to bind certain actions and methods in their
    code, the developer needs a way to follow a set of routines
    that guarantees a seamless integration with the front end
    of the application. This framework provides base classes
    to inherit from with a strict set of rules and methods
    already provided to make it easier for the application 
    to scale, as well as letting developers easily integrate
    their software to the front end with their own interfaces.

    To read instructions and see examples how to use this 
    framework with your application - please read the full
    documentation which can be found in the wiki on GitHub
"""

class FeatureCommandParserABC(ABC):
    """
    Describe a data structure that binds certain
    keywords to a certain feature. As the feature
    stack grows, this class is used as a template
    for base classes that work with decomposing 
    a message string, trying to understand its context
    and intent.
    """
    IGNORED_CHARS = '?=)(/&%¤#"!,.-;:_^*`´><|'

    def __init__(self, *args, **kwargs):
        self.ignored_chars = dict()
        super().__init__()
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @abstractmethod
    def __contains__(self, word: str) -> bool:
        return

    @abstractmethod
    def ignore_all(self, char: str):
        pass

    @abstractmethod
    def is_contender_for_processing(self, message: Message) -> bool:
        return
    
    @abstractmethod
    def get_callback(self, message: Message) -> 'function':
        return

    @property
    @abstractmethod
    def keywords(self) -> tuple:
        return
    
    @keywords.setter
    @abstractmethod
    def keywords(self, keywords: tuple):
        pass

    @property
    @abstractmethod
    def callbacks(self) -> dict:
        return

    @callbacks.setter
    @abstractmethod
    def callbacks(self, callbacks: dict):
        pass

    @property
    @abstractmethod
    def ignored_chars(self) -> dict:
        return

    @ignored_chars.setter
    @abstractmethod
    def ignored_chars(self, table: dict):
        pass

    @property
    @abstractmethod
    def interactive_methods(self) -> list:
        return
    
    @interactive_methods.setter
    @abstractmethod
    def interactive_methods(self):
        pass


class FeatureCommandParserBase(FeatureCommandParserABC):

    def __init__(self, *args, **kwargs):
        self._keywords = ()
        self._callback = {}
        self._ignored_chars = str()
        self._interactive_methods = ()
        
        super().__init__(*args, **kwargs)

    def __repr__(self):
        try:
            return f'FeatureCommandParser({self.callbacks})'
        except:
            return f'Warning: CommandParser not configured, missing callbacks.'

    def __contains__(self, word: str) -> bool:
        return word in self._keywords

    def ignore_all(self, char: str):
        self.ignored_chars[char] = ''

    def is_contender_for_processing(self, message: Message) -> bool:
        """
        Iterate over the words in received message, and 
        see if any of the words line up with the keywords
        provided for an instance of this class. If a match
        is found, return True, else False.
        """
        for key in self.ignored_chars:
            message.content = [word.replace(key, self._ignored_chars[key]) for word in message.content]

        for word in message.content:
            if word.strip(FeatureCommandParserBase.IGNORED_CHARS) in self:
                return True
        return False
    
    def get_callback(self, message: Message) -> Callback:
        """
        Returns the method (function object) bound to a 
        Callback object, if eligible. This method 
        should be overloaded if a different return behavior 
        in a no-match-found scenario is desired.
        """

        message.content = [i.strip(FeatureCommandParserBase.IGNORED_CHARS) for i in message.content]

        for cb in self._callbacks:
            match = cb.matches(message)
            if match: return cb
        return None

    @property
    def keywords(self) -> tuple:
        return self._keywords
    
    @keywords.setter
    def keywords(self, keywords: tuple):
        if isinstance(keywords, str):
            keywords = (keywords,)
        else:
            for i in keywords:
                if not isinstance(i, str):
                    raise TypeError(f'{_cim.warn}: keyword "{i}" must be str, got {type(i)}')
        self._keywords = keywords

    @property
    def callbacks(self) -> tuple:
        return self._callbacks
    
    @callbacks.setter
    def callbacks(self, callbacks: tuple):
        if isinstance(callbacks, Callback):
            callbacks = (callbacks,)
        self._callbacks = callbacks

    @property
    def ignored_chars(self) -> dict:
        return self._ignored_chars

    @ignored_chars.setter
    def ignored_chars(self, table: dict):
        if not isinstance(table, dict):
            raise TypeError(f'{_cim.warn}: category must be dict, got {type(table)}')
        self._ignored_chars = table
    
    @property
    def interactive_methods(self) -> tuple:
        return self._interactive_methods
    
    @interactive_methods.setter
    def interactive_methods(self, arg: tuple):
        sys.stdout.write(
            f"{_cim.deprecated_warn}: interactive methods are automated in CI 1.2.6 and needs no assignment"
        )


class FeatureABC(ABC):
    """ 
    Represent the template for a complete and 
    ready-to-use feature. 
    """
    def __init__(self, *args, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @abstractmethod
    def __call__(self, message: list):
        pass

    @property
    def mapped_pronouns(self) -> tuple:
        return

    @mapped_pronouns.setter
    def mapped_pronouns(self, pronouns: tuple):
        pass
    
    @property
    @abstractmethod
    def interface(self) -> object:
        return
    
    @interface.setter
    @abstractmethod
    def interface(self, interface: object):
        pass

    @property
    @abstractmethod
    def command_parser(self) -> FeatureCommandParserBase:
        return

    @command_parser.setter
    @abstractmethod
    def command_parser(self, command_parser: FeatureCommandParserBase):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, name: str):
        pass


class FeatureBase(FeatureABC):
    """
    Base class for features coupled to the chatbot. 
    Use this class as a base class to inherit from when
    connecting your feature's interface to the bot.
    """

    def __init__(self, *args, **kwargs):
        self._command_parser = None
        self._interface = None
        self._name = None
        self._mapped_pronouns = ()
        super().__init__(*args, **kwargs)

    def __call__(self, message: Message) -> callable:
        try:
            feature_function = self._command_parser.get_callback(message)
            if feature_function is None:
                return None

            if feature_function in self._command_parser.interactive_methods:
                return lambda message = message: feature_function(message)
        except KeyError:
            raise NotImplementedError(f'{_cim.warn}: no mapped function call for {feature_function} in self')

        return feature_function

    def __repr__(self):
        if self._name:
            return f'Feature(Feature{self.name})'
        return f'Feature({type(self).__name__})'
    
    @property
    def mapped_pronouns(self) -> tuple:
        return self._mapped_pronouns

    @mapped_pronouns.setter
    def mapped_pronouns(self, pronouns: tuple = ()):
        if not isinstance(pronouns, tuple):
            raise TypeError(f'{_cim.warn}: pronouns must be enclosed in a tuple, got {type(pronouns)}')
                
        self._mapped_pronouns = list(pronouns)
        self._mapped_pronouns.insert(0, CommandPronoun.UNIDENTIFIED)
        self._mapped_pronouns = tuple(self._mapped_pronouns)

    @property
    def interface(self) -> object:
        return self._interface
    
    @interface.setter
    def interface(self, interface: object):
        self._interface = interface

    @property
    def command_parser(self) -> FeatureCommandParserBase:
        return self._command_parser

    @command_parser.setter
    def command_parser(self, command_parser: FeatureCommandParserBase):
        if not isinstance(command_parser, FeatureCommandParserBase):
            raise TypeError(f'{_cim.warn}: command_parser must inherit from FeatureCommandParserBase')
        self._command_parser = command_parser

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name