from enum import Enum


class GrammaticalAspect(Enum):
    """ Enumeration of the grammatical aspect of a :@link IWiktionaryWordForm.
        Note that tense is often combined with verb aspects (e.g., present
        perfect). Such combinations can be modeled in combination with
        enumeration values from :@link GrammaticalTense. """

    """ An ongoing, habitual, repeated situation. Used to express the 
        English simple forms (e.g., "I paint the house") and 
        progressive forms ("I am painting the house"). The imperfect 
        aspect is also used for the German "Partizip I" form 
        (e.g. "die liebende Mutter").  """
    IMPERFECT = 1

    """ A completed situation. Used to express the English perfect forms 
        (e.g., "I have painted the house"). The perfect aspect is also 
        used for the German "Partizip II" form 
        (e.g., "die geliebte Mutter"). """
    PERFECT = 2

#    Perfective
#        Aorist
#        Momentane
#        Semelfactive
#    Imperfective
#        Continuous and progressive
#        Durative
#        Imperfect
#        Iterative/distributive/frequentative

    def __str__(self):
        return str(self.name)
