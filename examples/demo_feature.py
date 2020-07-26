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
        self.command_parser.keywords = ('what')
        self.command_parser.callbacks = ci.Callback(
            lead = ('time', 'tiden'), 
            trail = ('is', 'it'), func = self.get_time
        )

    @ci.logger.loggedmethod
    def get_time(self):
        ci.logger.log(message = "This was run by the inherited feature", level = "info")
        return f'Klockan är {time.strftime("%H:%M")}.'

#  ------------------------------------------------------------
#  -- DEVELOP FEATURES USING INHERITATION:
#  ->> EXAMPLE #2 :


class VulcanTranslatorFeature(ci.FeatureBase):

    FEATURE_KEYWORDS = (
        'översätt',
        'översätta',
        'translate'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.command_parser = ci.CommandParser()
        self.command_parser.keywords = VulcanTranslatorFeature.FEATURE_KEYWORDS
        self.command_parser.callbacks = ci.Callback(
            lead = ('översätt', 'översätta', 'translate'), 
            func = self.translate
        )
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



if __name__ == '__main__':
    
    #  ------------------------------------------------------------
    #  -- DEVELOP FEATURES USING DEAFULT OBJECTS:
    #  ->> EXAMPLE #1 :
    
    vulcan_api_url = "https://api.funtranslations.com/translate/vulcan.json"
    vulcan_api_handle = ci.RestApiHandle(vulcan_api_url)

    # Interactive methods (will be fed the Message object from front end for processing)
    @ci.logger.loggedmethod
    def translate(message: ci.Message) -> str:
        """
        life, is, like, a, box, of, chocolates
        """
        message.content = message.content[1:]

        for i in message.content:
            stripped = i.strip(ci.CommandParser.IGNORED_CHARS)

        msg = str(' ').join(message.content)
        headers = {'text': msg}
        res = vulcan_api_handle.post(headers)
        return str().join(res['contents']['translated'])

    # Normal methods (takes 0 arguments)
    @ci.logger.loggedmethod
    def get_time():
        ci.logger.log(message = "This was run by the non-inherited feature", level = "info")
        return f'Klockan är {time.strftime("%H:%M")}.'
    
    msg = ci.Message()
    processor = ci.CommandProcessor()

    # Instantiate features from classes above, that inherited base classes:
    clock_feature_inherit = ClockFeature()
    vulcan_feature_inherit = VulcanTranslatorFeature()

    # Instantiate features using default objects (different approach):
    clock_feature_basic = ci.Feature(name = 'ClockFeature_Basic')
    vulcan_feature_basic = ci.Feature(name = 'VulcanTranslatorFeature_Basic')

    # The Vulcan feature needs the message to translate it, 
    # Adding it to the .interactive_methods property to enable
    # this method to receive the parameter "message".
    vulcan_feature_basic.interactive_methods = (translate,)

    # Instantiate command parser object for these features:
    clock_feature_basic.command_parser = ci.CommandParser(
        keywords = ('klockan', 'time', 'echo'),
        callbacks = {'klockan': get_time, 'time': get_time}
    )

    vulcan_feature_basic.command_parser = ci.CommandParser(
        keywords = ('översätt', 'translate'),
        callbacks = {'översätt': translate, 'translate': translate}
    )


    # --- Start the virtual assistant ---

    # Assign features to the CommandProcessor.
    processor.features = (vulcan_feature_basic, clock_feature_basic)
    
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