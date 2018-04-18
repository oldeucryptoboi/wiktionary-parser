import re
from compat import Set


class StringUtils:
    """ Set of static string-processing methods used throughout the software.  """

    @staticmethod
    def split(text, divider):
        """ Creates a new string array from the given string, in which each
            field corresponds to a token of the input text. Tokens are separated
            from each other by the specified divider character. The method thus
            corresponds to its perl sibling. It may be used for processing
            tabular- or comme-separated files. """
        fieldCount = 1
        for c in text:
            if c == divider:
                fieldCount += 1

        result = []
        idx = 0
        while True:
            i = text.find(divider)
            if i >= 0:
                result[idx] = text[0:i]
                idx += 1
                text = text[i + 1:]

            if i < 0:
                break

        result[idx] = text
        return result

    @staticmethod
    def strip(text, characters):
        """ Removes the specified characters from the left and right of the
            specified text. The method thus corresponds to the trim function,
            but with arbitrary characters. """
        result = text
        while result and result[0] in characters:
            result = result[1:]
        while result and result[-1] in characters:
            result = result[:- 1]
        return result

    LITERATURE_PATTERN = re.compile("\\{\\{Literatur\\|[^}]+\\}\\}|<ref[^>]*>.*?</ref>")

    @staticmethod
    def removeReferences(text):
        """ Removes all references or literature patterns from the given input
            text. """
        return re.sub(StringUtils.LITERATURE_PATTERN, "", text)

    @staticmethod
    def compileIndexSet(indexedStr):
        """ Parses a string representation of index numbers and returns a set of
            integers containing all numbers of the specified range. The method
            is capable of handling single numbers ("23" -> :23), multiple comma-,
            or full-stop-separated numbers ("1,2. 4" -> :1,2,4", and number
            ranges ("1-4" -> :1,2,3,4). """
        result = Set()
        lastIdx = -1
        currIdx = -1
        for c in indexedStr:
            if '0' <= c <= '9':
                if currIdx < 0:
                    currIdx = 0
                currIdx = currIdx * 10 + ord(c) - ord('0')
            elif c == ',' or c == '.':
                if lastIdx >= 0:
                    for idx in range(lastIdx, currIdx+1):
                        result.add(idx)
                    lastIdx = -1
                else:
                    result.add(currIdx)
                currIdx = 0
            elif c == '-' or c == '–':
                lastIdx = currIdx
                currIdx = 0

        if lastIdx >= 0:
            for idx in range(lastIdx, currIdx+1):
                result.add(idx)
            # lastIdx = -1
        else:
            result.add(currIdx)
        return result

    @staticmethod
    def cleanText(text):
        result = StringUtils.stripMarkup(text)
        return result.strip()

    @staticmethod
    def stripMarkup(text):
        result = text
        result = result.replace("[[", "")
        result = result.replace("]]", "")
        result = result.replace("'''", "")
        result = result.replace("''", "")
        return result
