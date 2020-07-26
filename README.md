# CommandIntegrator

## What it does
CommandIntegrator is a lightweight framework and API for creating apps controlled with commands.
It concists of base classes and ready-to-use objects along with a set and clear structure for how to develop and scale a chat bot / Virtual assistant. 

Objects such as the `Feature`, which can be thought of a micro service within your app, makes it easier to keep the OOP structure clean and well maintained. Automatic command parsing with the `CommandParser` and `CommandProcessor` makes it very  straight forward to build and scale your command-controlled application without having to worry about name and word collisions, edge-case actions etcetera.



## Objects and wrappers for more effective and easier development

CommandIntegrator comes with objects to make development easier.  Decorator wrappers for automated logging, scheduling of function execution, caching objects and API DAO's are a few that are included in the package.



## Example

Here's a short example of how to create a virtual assistant that tells you what time it is.
For a more comprehensive example, please read the `demo_feature.py` file in /examples, or 
refer to the Wiki.

```python
import CommandIntegrator as ci
import time

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
```



## Changelog



#### CommandIntegrator version 1.2.6

​	

This patch contains news and improvements.

**Important**: Features without `Callback` as the object in `callbacks `for `CommandParser` objects will not work, and need to be upgraded to `Callback`.



**New**

*  `Callback`  
  The `Callback` object has replaced the old structure with dictionaries when creating a callback binding with words to a method in Features. See `demo_feature` in `examples.py` for a demo of how to get started and upgrading your features.
* Compliance in *FeatureBase*, *CommandParserBase* and *CommandProcessor for use with `Callback`
  
  

**Improvements**

* Fixes an issue where no warning was delivered upon trying to use **int** as key in callbacks. This is still not supported but is now explained through an error.
* Fixes an issue with Features receiving the lowered version of the command only. Features still match case insensitive but now receive the original message.







#### CommandIntegrator 1.2.5 update

**New**

* `CommandParser	` Class, ready-to-use. See **example.py** in **/examples** 

  If you only need a default CommandParser without any overloaded methods, this class is for you!

  You no longer need to inherit the FeatureCommandParserBase in order to create a command parser

  for your Feature, just use the `CommandParser` object.
  
* `Feature` Class, ready-to-use. See **example.py** in **/examples** 

* The `FeatureCommandParserBase` is no longer mandatory to inherit from. You can simply use the `CommandParser` object which is included in the package.
  
* The `PronounLookupTable` class is no longer needed. It is present but changed to a **static** type which is accessed by the `CommandProcessor`.
  

**Improvements**

* `import CommandIntegrator` is now the only needed import to access everything within the package. By the use of the `__init__.py` file. `import CommandIntegrator as ci` will give you access to all classes and functions in the package from the `ci.` syntax

  

* Language data is migrated to a new file called `language.json` which allows developers to easily increase the support for other languages
  
* Code refactoring including module details, module name scheme according to PEP8
  
* Pronoun strings removed from `PronounLookupTable` object and moved to `language.json` 
  
*  Create log entries manually using:
   `@ci.logger.log(message, level = "debug"  / "info" / "error")`
* Set log file location and name in `commandintegrator.settings`
  
* Choose whether or not to **append** the log file (**false** evaluates to file overwrite each start)
  
* `CommandProcessor` now accepts a single feature without being enclosed in Tuple.
  
* Reduced processing time of commands
  
* Reduced code needed to create a working assistant with command integration
  
* `logger` function is rewritten as a class

* You can now log manual entries by calling:

   `ci.logger.log(message = "Derp", level = "debug" # "info" # "error")`


* The decoration to use changed from `@logger` to `@ci.logger.loggedmethod`
