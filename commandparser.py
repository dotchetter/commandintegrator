from .baseclasses import FeatureCommandParserBase

class CommandParser(FeatureCommandParserBase):
    """
    Class with attributes and methods from the base
    class FeatureCommandParserBase, to be used when
    no method overloading is desired by the developer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

