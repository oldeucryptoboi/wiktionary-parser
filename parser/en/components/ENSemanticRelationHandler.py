from parser.util import SimilarityUtils
from parser.en.components.ENRelationHandler import ENRelationHandler
from api.entry import WikiString


class ENSemanticRelationHandler(ENRelationHandler):
    """ Parser component for extracting
        <a href="https://en.wiktionary.org/wiki/Wiktionary:Semantic_relations">semantic relations</a>
        from the English Wiktionary.

        A semantic relation ship can specify a target sense. This handler tries to determine the target
        sense using :@link #findMatchingSense(WiktionaryEntry, String). """

    def __init__(self, relationType, *labels):
        super().__init__(relationType, *labels)

    def findMatchingSense_(self, posEntry, wordList):
        matchingSense = self.findMatchingSense(posEntry, wordList.comment)

        if matchingSense is not None:
            return matchingSense
        else:
            return super().findMatchingSense_(posEntry, wordList)

    @classmethod
    def findMatchingSense(cls, entry, marker):
        """ @return the word sense whose sense definition
            corresponds to the specified comment (sense marker). The matching
            of the corresponding word sense is achieved by word similarity
            metrics. Returns <code>None</code> if no matching word sense
            could be found. """
        if entry.getSenseCount() == 1:
            return entry.getSense(1)

        # Empty sense marker.
        if marker is None or not len(marker):
            return None

        best1Gram = None
        best3Gram = None
        best1GramScore = -1
        best3GramScore = -1

        for sense in entry.senses:
            if sense.getIndex() <= 0:
                continue  # Skip unassigned sense.

            gloss = WikiString.removeWikiLinks(sense.getGloss().getText()).lower()
            similarity = SimilarityUtils.wordSim(marker, gloss)
            if similarity > best1GramScore:
                best1GramScore = similarity
                best1Gram = sense

            similarity = SimilarityUtils.textSim(marker, gloss)
            if similarity > best3GramScore:
                best3GramScore = similarity
                best3Gram = sense

        if best1Gram is None and best3Gram is None:
            return None

        if best1GramScore <= 0 and best3GramScore <= 0:
            return None

        if best1GramScore > best3GramScore:
            return best1Gram
        else:
            return best3Gram
