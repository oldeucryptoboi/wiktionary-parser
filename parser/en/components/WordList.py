import re
from parser.util import WordListProcessor
from compat import Iterable, Iterator
from errors import NullPointerException


class WordList(Iterable):

    PATTERN_WORD = re.compile("\\w+")  

    def __init__(self, comment, words):
        self.comment = comment if self.isValid(comment) else None
        self.words = words

    def __len__(self):
        return len(self.words)

    @classmethod
    def parse(cls, text):
        if text is None:
            raise NullPointerException()

        comment = None
        result = list()

        braceStartIndex = text.find("(''")
        if braceStartIndex == -1:
            braceStartIndex = text.find("(")

        curlyStartIndex = text.find("{{")
        curlyEndIndex = text.find("}}")
        endIndex = -1
        if (braceStartIndex != -1 and curlyStartIndex == -1) or (braceStartIndex != -1 and braceStartIndex < curlyStartIndex):
            endOffset = 3
            braceEndIndex = text.find("'')", braceStartIndex)
            if braceEndIndex == -1:
                braceEndIndex = text.find(")", braceStartIndex)
                endOffset = 1
            
            if braceEndIndex == -1:
                braceEndIndex = text.find("''", braceStartIndex+3)
                endOffset = 2
            
            if braceStartIndex + endOffset < braceEndIndex:
                s = text[braceStartIndex+endOffset: braceEndIndex]
                endIndex = braceEndIndex + endOffset
                comment = s
            
        elif curlyStartIndex != -1 and curlyEndIndex != -1 and curlyEndIndex >= curlyStartIndex:
                midIndex = text.find('|', curlyStartIndex)
                if midIndex != -1 and midIndex < curlyEndIndex:
                    templateName = text[curlyStartIndex + 2: midIndex]
                    if "l" != templateName and not templateName.startswith("l/"):
                        comment = text[midIndex + 1:curlyEndIndex]
                    
                else:
                    comment = text[curlyStartIndex + 2:curlyEndIndex]
                
        wordListFilter = WordListProcessor()
        if 0 < endIndex < len(text):
            relationStr = text[endIndex:]
        elif endIndex == -1:
            relationStr = text
        else:
            return WordList(comment, result)

        result.extend(wordListFilter.splitWordList(relationStr))
        return WordList(comment, result)
    
    def iterator(self):
        return Iterator(self.words)

    @staticmethod
    def isValid(comment):
        return comment is not None and re.search(WordList.PATTERN_WORD, comment) is not None
