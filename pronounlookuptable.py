from .enumerators import CommandPronoun

class PronounLookupTable:
    """
    Provide a grammatic lookup that 
    returns a tuple of matches for certain
    grammatic classes of words found in a given
    sentence. 
    """

    _LOOKUP_TABLE = {
        CommandPronoun.INTERROGATIVE: (
            'vad', 'vem',
            'hur', 'varför',
            'vilken', 'vilket',
            'hurdan', 'hurudan',
            'undrar', 'när'),

        CommandPronoun.PERSONAL: (
            'jag', 'vi',
            'du', 'ni',
            'han', 'hon',
            'den', 'de',
            'dem'),

        CommandPronoun.POSSESSIVE: (
            'mitt', 'mina',
            'min', 'vårt',
            'vår', 'våra',
            'vårt', 'din',
            'ditt', 'dina',
            'ert', 'er',
            'era', 'sin',
            'sitt', 'sina')
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
        """
        pronouns = []

        for word in message:
            for key in PronounLookupTable._LOOKUP_TABLE:
                if word in PronounLookupTable._LOOKUP_TABLE[key]:
                    pronouns.append(key)
            if '?' in word:
                pronouns.append(CommandPronoun.INTERROGATIVE)

        if len(pronouns):
            return tuple(sorted(set(pronouns)))
        return (CommandPronoun.UNIDENTIFIED,)
