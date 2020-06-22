import pytz
import random
import json
import traceback
import sys

import models
from ast import literal_eval
from pprint import pprint
from os import system
from datetime import datetime, timedelta, time
from enum import Enum, auto
from abc import ABC, abstractmethod
from .enumerators import CommandPronoun


"""
Details:
    2020-006-21
    
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
    def is_contender_for_processing(self, message: discord.Message) -> bool:
        return
    
    @abstractmethod
    def get_callback(self, message: discord.Message) -> 'function':
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
        self.interactive_methods = tuple()
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

    def is_contender_for_processing(self, message: discord.Message) -> bool:
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
    
    def get_callback(self, message: discord.Message) -> 'function':
        """
        Returns the method (function object) bound to a 
        subcategory in the feature implementation. This method 
        should be overloaded if a different return behavior 
        in a no-match-found scenario is desired.
        """

        strip_chars = lambda string: string.strip(FeatureCommandParserBase.IGNORED_CHARS)
        complex_subcategories = []
        simple_subcategories = []
        
        for key in self._callbacks.keys():
            try:
                complex_subcategories.append(literal_eval(key))
            except:
                simple_subcategories.append(key)


        for subcategory in complex_subcategories:
            for word in message.content:
                word = strip_chars(word)
                try:
                    subset = subcategory[word]
                except KeyError:
                    pass
                else:
                    if [strip_chars(i) for i in message.content if strip_chars(i) in subset]:
                        return self._callbacks[str(subcategory)]
    
        for word in message.content:
            word = strip_chars(word)
            if word in simple_subcategories:
                return self._callbacks[word]
        return None

    @property
    def keywords(self) -> tuple:
        return self._keywords
    
    @keywords.setter
    def keywords(self, keywords: tuple):
        if not isinstance(keywords, tuple):
            raise TypeError(f'{_cim.warn}: keywords must be tuple, got {type(keywords)}')
        for i in keywords:
            if not isinstance(i, str):
                raise TypeError(f'{_cim.warn}: keyword "{i}" must be str, got {type(i)}')
        self._keywords = keywords

    @property
    def callbacks(self) -> dict:
        return self._callbacks
    
    @callbacks.setter
    def callbacks(self, callbacks: dict):
        if not isinstance(callbacks, dict):
            raise TypeError(f'{_cim.warn}: callbacks must be dict, got {type(callbacks)}')
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
        if not isinstance(arg, tuple):
            raise TypeError(f'{_cim.warn}: interactive methods must be enclosed in tuple, got {type(arg)}')
        for i in arg:
            if not callable(i):
                raise TypeError(f'{_cim.warn}: interactive method not callable: {i}')
            elif 'lambda' in i.__name__:
                raise KeyError(f'{_cim.warn}: interactive method wrapped in lambda: {i.__module__}')
        self._interactive_methods = arg

class CommandParser(FeatureCommandParserBase):
    """
    Class with attributes and methods from the base
    class FeatureCommandParserBase, to be used when
    no method overloading is desired by the developer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


class FeatureBase(FeatureABC):
    """
    Base class for features coupled to the chatbot. 
    Use this class as a base class to inherit from when
    connecting your feature's interface to the bot.
    """

    def __init__(self, *args, **kwargs):
        self.interactive_methods = tuple()
        super().__init__(*args, **kwargs)

    def __call__(self, message: discord.Message) -> callable:
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
        return f'Feature({__class__.__name__})'
    
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
    def process(self, message: discord.Message) -> Interpretation:
        """
        Part of the public interface. This method takes a discord.Message
        object  and splits the .content property on space characters
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
   
    def _interpret(self, message: discord.Message) -> Interpretation:
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