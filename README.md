# CommandIntegrator

## What it does
CommandIntegrator is a lightweight framework and API for creating apps controlled with human language interfaces.
It concists of base classes and ready-to-use objects along with a set and clear structure for how to develop and scale a chat bot / Virtual assistant. 

Objects such as the `Feature`, which can be thought of a micro service within your app, makes it easier to keep the OOP structure clean and well maintained. Automatic command parsing with the `CommandParser` and `CommandProcessor` makes it very  straight forward to build and scale your command-controlled application without having to worry about name and word collisions, edge-case actions etcetera.



## Objects and wrappers for more effective and easier development

CommandIntegrator exists for one reason: To make development of language-driven apps easier.  Decorator wrappers for automated logging, scheduling of function execution, caching objects and API DAO's are a few that are included in the package.

You can build the backend of your virtual assistant / chatbot with the tools and structures of CommandIntegrator and use it in your chatbot for whichever platform you want to use. CommandIntegrator is platform independent and can be used even with a simple command-line app as demonstrated below.


## Example

Here's a short example of how to create a virtual assistant that tells you what time it is.
For a more comprehensive example, please read the `demo_feature.py` file [here](https://github.com/dotchetter/CommandIntegrator/blob/master/examples/demo_feature.py)

```python
import CommandIntegrator as ci
import time
from pprint import pprint

class ClockFeature(ci.FeatureBase):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.command_parser = ci.CommandParser()

        # Defines which keywords that this Feature identifies with initially
        self.command_parser.keywords = ('what')

        # The Callback object is a more intricate and well defined way of 
        # binding a sentence / sequence of words to a function. 
        self.command_parser.callbacks = ci.Callback(lead = 'time', trail = ('is', 'it'), func = self.get_time)

    @ci.logger.loggedmethod
    def get_time(self):
        ci.logger.log(message = "Manual log entry here", level = "info")
        return f'The time is {time.strftime("%H:%M")}.'
    
    
    
if __name__ == '__main__':
    processor = ci.CommandProcessor()
    processor.features = (ClockFeature(),)
    msg = ci.Message()
    
    while True:
        msg.content = input("-> ")
        response = processor.process(msg)
        
        print("\n-> Response received:\n")
        pprint(f"\t{response.__dict__}")
        print("\n-> Bot said: ", response.response(), "\n")
```