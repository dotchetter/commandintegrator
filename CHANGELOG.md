
# Changelog


##  Version 1.2.8

* Fixes an issue introduced in 1.2.7 where asynchronous tech stacks would hang with the new implementation of deepcopy used in patch 1.2.7

##  Version 1.2.7

* Fixes an issue introduced in 1.2.6 where the message content collection would be affected in the processing of the message, causing it to lack special characters
* Fixes a documentation error where the wrong type hinting was used in the Message object
* Fixes a bad design choice where the module would call sys.exit() unless requirements were met for CommandProcessor upon import


##  Version 1.2.6

This patch contains news and improvements.

**Important**: Features without `Callback` as the object in `callbacks `for `CommandParser` objects will not work, and need to be upgraded to `Callback`.
**New**
* Callback 
The `Callback` object has replaced the old structure with dictionaries when creating a callback binding with words to a method in Features. See `demo_feature` in `examples.py` for a demo of how to get started and upgrading your features.
* Compliance in *FeatureBase*, *CommandParserBase* and *CommandProcessor for use with `Callback`
* The **interactive_methods** tuple property for CommandParser objects is deprecated, and replacedb by the **interactive** flag for the **Callback** object.

**Improvements**
* Fixes an issue where no warning was delivered upon trying to use **int** as key in callbacks. This is still not supported but is now explained through an error.
* Fixes an issue with Features receiving the lowered version of the command only. Features still match case insensitive but now receive the original message.

##  Version 1.2.5

**New**

* CommandParser class, ready-to-use. See **example.py** in **/examples** 

  If you only need a default CommandParser without any overloaded methods, this class is for you.
  You no longer need to inherit the FeatureCommandParserBase in order to create a command parser

  for your Feature, just use the `CommandParser` object.
  
* `Feature` Class, ready-to-use. See **example.py** in **/examples** 

* The `FeatureCommandParserBase` is no longer mandatory to inherit from. You can simply use the `CommandParser` object which is included in the package.
  
* The `PronounLookupTable` class is no longer needed. It is present but changed to a **static** type which is accessed by the `CommandProcessor`.
  

**Improvements**

* `import commandintegrator` is now the only needed import to access everything within the package. By the use of the `__init__.py` file. `import commandintegrator as ci` will give you access to all classes and functions in the package from the `ci.` syntax


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
