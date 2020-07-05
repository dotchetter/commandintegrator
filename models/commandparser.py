from ..baseclasses.baseclasses import FeatureCommandParserBase

"""
Details:
    2020-07-05
    
    CommandIntegrator framework CommandParser source file

Module details:
    
    The CommandParser object is a ready-to-use
    variant of the FeatureCommandParserBase class
    which is designed for inheritation. Using the
    CommandParser object enables developers to 
    use the default configuration of the CommandParser
    without writing a trivial inherit with only
    a constructor for child and parent class, allowing
    for two ways to develop with CommandIntegrator.
"""

class CommandParser(FeatureCommandParserBase):
    """
    Class with attributes and methods from the base
    class FeatureCommandParserBase, to be used when
    no method overloading is desired by the developer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

