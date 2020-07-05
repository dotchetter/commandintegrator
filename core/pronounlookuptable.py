from .enumerators import CommandPronoun
from .internals import _cim
import sys

"""
Details:
    2020-07-05
    
    CommandIntegrator framework PronounLookupTable source file

Module details:
    
    The PronounLookupTable object is built to work
    statically as a way to identify pronouns in 
    a scentence, with the ultimate goal to make
    developing command driven applications using
    pronouns easier, by aiding in the identification
    of pronouns in a scentence - either for training
    ML models, knowing what the user is saying beyond
    keyword matching, etcetera.
"""

class PronounLookupTable:
    """
    Provide a grammatic lookup that 
    returns a tuple of matches for certain
    grammatic classes of words found in a given
    sentence. 
    """

    LOOKUP_TABLE = {
        CommandPronoun.INTERROGATIVE: tuple(),
        CommandPronoun.PERSONAL: tuple(),
        CommandPronoun.POSSESSIVE: tuple()
    }

    @staticmethod
    def lookup(message: list) -> tuple:
        """
        Split a given string by space if present, to iterate
        over a sentence of words. Returns a tuple with enum
        instances representing the pronouns that make up the
        composition of the string received. If none is found,
        a tuple with a single CommandPronoun.UNIDENTIFIED is 
        returned.

        :param message:
            list with words (string split on space) for pronoun
            identification
        :returns:
            tuple containing identified pronouns, represented by
            Enum instance(s) of CommandPronoun.
        """
        pronouns = []

        for key in PronounLookupTable.LOOKUP_TABLE.keys():
            if not len(PronounLookupTable.LOOKUP_TABLE[key]):
                raise NotImplementedError(
                    f'{_cim.warn}: PronounLookupTable is missing pronoun lookups. ' \
                     'Ensure language.json is present and is valid. Use ' \
                     'assign_pronoun_identifiers to set pronouns or refer to ' \
                     'the documentation for CommandIntegrator on PronounLookupTable.'
                )

        for word in message:
            for key in PronounLookupTable.LOOKUP_TABLE:
                if word in PronounLookupTable.LOOKUP_TABLE[key]:
                    pronouns.append(key)
            if '?' in word:
                pronouns.append(CommandPronoun.INTERROGATIVE)

        if len(pronouns):
            return tuple(sorted(set(pronouns)))
        return (CommandPronoun.UNIDENTIFIED,)

    @staticmethod
    def assign_pronoun_identifiers(identifiers: dict, language: str) -> None:
        """
        Configure the pronoun lookup table from provided
        dict, binding them to CommandPronoun enum instances
        for fast lookups.
        
        :param identifiers:
            dict, containing structure with pronouns where
            expected keys are: 
            "interrogative", "personal", "possessive" - with
            Lists of words as values.
        :param language:
            str, format: "en-us", "sv-se", etcetera
        :returns:
            None
        """

        PronounLookupTable.LOOKUP_TABLE[CommandPronoun.PERSONAL] = tuple(identifiers[language]['personal'])
        PronounLookupTable.LOOKUP_TABLE[CommandPronoun.INTERROGATIVE] = tuple(identifiers[language]['interrogative'])
        PronounLookupTable.LOOKUP_TABLE[CommandPronoun.POSSESSIVE] = tuple(identifiers[language]['possessive'])

