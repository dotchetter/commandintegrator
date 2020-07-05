import sys
import CommandIntegrator as ci
import time
from pprint import pprint

"""
Details:
    2020-07-05
    
    CommandIntegrator framework Demo source file

Module details:
    
    In this file, you can see a few examples of 
    how you can develop with CommandIntegator!

    The approach to go the inherit route (recommended)
    or, the more pythonic and simple way where everything
    is set up for you - using the pre-written standard
    objects and dynamically assigning values to them.

    Please note that this code should be moved to the same
    directory as the CommandIntegator package for the import
    to work.
"""

#  ------------------------------------------------------------
#  -- DEVELOP FEATURES USING INHERITATION:
#  ->> EXAMPLE #1:

class ClockFeatureCommandParser(ci.FeatureCommandParserBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ClockFeature(ci.FeatureBase):

    # This Feature enables the assistant system to 
    # return the current time when you ask it. 

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)        
        self.mapped_pronouns = (ci.CommandPronoun.INTERROGATIVE,)
        self.command_parser = ci.CommandParser()
        self.command_parser.keywords = ('time', 'clock')
        self.command_parser.callbacks = {'time': self.get_time,
                                        'tiden': self.get_time}

#  ------------------------------------------------------------
#  -- DEVELOP FEATURES USING INHERITATION:
#  ->> EXAMPLE #2 :

class VulcanTranslatorFeatureCommandParser(ci.FeatureCommandParserBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VulcanTranslatorFeature(ci.FeatureBase):

    FEATURE_KEYWORDS = (
        'översätt',
        'översätta',
        'translate'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.command_parser = VulcanTranslatorFeatureCommandParser()
        self.command_parser.keywords = VulcanTranslatorFeature.FEATURE_KEYWORDS
        self.command_parser.callbacks = {
            'translate': self.translate,
            'översätt': self.translate,
            'översätta': self.translate
        }

        self.command_parser.interactive_methods = (self.translate,)
        self.apihandle = ci.RestApiHandle("https://api.funtranslations.com/translate/vulcan.json")

    @ci.logger.loggedmethod
    def translate(self, message: ci.Message) -> str:
        """
        life, is, like, a, box, of, chocolates
        """

        for i in message.content:
            stripped = i.strip(self.command_parser.IGNORED_CHARS)
            if stripped in self.command_parser.keywords:
                message.content.remove(i)

        msg = str(' ').join(message.content)
        headers = {'text': msg}
        res = self.apihandle.post(headers)
        return str().join(res['contents']['translated'])


#  ------------------------------------------------------------
#  -- DEVELOP FEATURES USING DEAFULT OBJECTS:
#  ->> EXAMPLE #1 :

# Interactive methods (will be fed the Message object from front end for processing)
@ci.logger.loggedmethod
def echo(message: ci.Message) -> str:
    return f'You said: {message.content}'

# Normal methods (takes 0 arguments)
@ci.logger.loggedmethod
def get_time():
    ci.logger.log(message = "I logged this manually.", level = "info")
    return f'Klockan är {time.strftime("%H:%M")}.'

# Instantiate a CommandParser, Feature and assign Keywords and Callbacks
clock_feature = ci.Feature(name = 'ClockFeature')
command_parser = ci.CommandParser()

command_parser.keywords = ('klockan', 'time', 'echo') 
command_parser.callbacks = {'klockan': get_time, 'time': get_time, 'echo': echo}
command_parser.interactive_methods = (echo,)

clock_feature.command_parser = command_parser

if __name__ == '__main__':
    
    msg = ci.Message()
    processor = ci.CommandProcessor()
    
    clock_feature = clock_feature
    vulcan_feature = VulcanTranslatorFeature()

    processor.features = (clock_feature,)
    
    print(f'\n# Running CommandIntegrator version: {ci.VERSION}')
    print('# Features loaded: ', '\n')
    [print(f'  - {i}') for i in processor.features]
    print(f'\n# Write a message and press enter, as if you were using your app front end.')
    
    while True:
        msg.content = input("-> ")
        if not msg.content:
            sys.exit()
        response = processor.process(msg)
        
        print("\n-> Response received:\n")
        pprint(f"\t{response.__dict__}")
        print("\n-> Bot said: ", response.response(), "\n")