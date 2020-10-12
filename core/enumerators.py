from enum import Enum, auto

"""
Details:
    2020-07-05
    
    commandintegrator framework CommandPronoun source file

Module details:
    
    The CommandPronoun Enum is used by the PronounLookupTable
    class while identifying pronouns in a given scentence /
    command. 
"""

class CommandPronoun(Enum):
    """
    Identifiable pronouns in recieved commands.
    __lt__ is implemented in order for a sorted
    set of instances to be returned.
    """
    INTERROGATIVE = auto()
    PERSONAL = auto()
    POSSESSIVE = auto()
    UNIDENTIFIED = auto()

    def __lt__(self, other):
        return self.value < other.value