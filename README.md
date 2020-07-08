# CommandIntegrator

CommandIntegrator is a lightweight framework for creating applications with Features that use commands in human languages, to bind them with certain methods, by creating a streamlined development structure with automated command parsing, logging, and more. 


## Explain?

CommandIntegrator includes both base classes to inherit from when creating "Features", which are classes that represent the interface of a certain feature that the application may have.
For example, if you build a virtual assistant that can tell you what time it is by asking it - that's a feature. Another one might be, telling you the weather forecast 
upon request.
Base classes for these purposes with pre-defined methods that automate the command parsing - that is, understanding the command and directing it to the correct
Feature and method in said feature. 

Aside from the framework itself for developing Feautres, the processing of the command is also automated by the CommandProcessor object. 
Simply pass instances of your Feature classes to this object on instantiation and pass your command to the CommandProcessor instance. 

## Objects and wrappers for more effective and easier development
Isn't t a hassle to implement a stupid simple, pragmatic yet bullet proof logging system for your project? 
If you're many developers on the same project, making sure that you all participate in a unified and clear
logging fashion without overwriting one another can be tricky. 

The logger wrapper in CommandIntegrator makes it incredibly easy to implement logging to your tech stack.
Simply import logger from CommandIntegrator, add @logger above the method declaration and have automated logging. Enjoy.

Things such as PollCache for acting as a Buffer between caller and responder, where output is only recieved if there's an update
in the response body, which is useful when asking an API or a website multiple times per hour, minute or second - but you only want
to hear it if there's actually an update.

The objects in the apihandle module which make use of the requests library among others, to make it super simple to interact with REST APIs.

These are a few things that make CommandIntegrator what is is. 





## CommandIntegrator 1.2.5 update changelog

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



