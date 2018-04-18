import re


class WordListProcessor:
    """ Helper class for segmenting word lists separated by comma, semicolon,
        line breaks, etc. This is, for example, the case for semantic relations
        which are often encoded as comma-separated lists. """

    HTML_REMOVER = re.compile("<[^>]+>")  
    ESCAPE_DELIMITER1 = re.compile("(\\[\\[[^\\]⁋]*)⁋([,;][^\\]⁋]*\\]\\])")  
    ESCAPE_DELIMITER2 = re.compile("(\\{\\{[^\\}⁋]*)⁋([,;][^\\}⁋]*\\}\\})")
    ESCAPE_DELIMITER3 = re.compile("(''[^'⁋]*)⁋([,;][^'⁋]*'')")  
    REFERENCE_PATTERN = re.compile("<ref>.*?</ref>")
    SUPERSCRIPT_PATTERN = re.compile("<sup>\\[\\d+\\]</sup>")

    @staticmethod
    def escapeDelimiters(text):
        result = ""
        inComment = False
        commentStart = ""
        commentEnd = ""
        for c in text:
            if not inComment:
                # Find comment start markers.
                if c == '[':
                    if "[" == commentStart:
                        commentStart = "[["
                        inComment = True
                    else:
                        commentStart = "["
                elif c == '{':
                    if "{" == commentStart:
                        commentStart = "{{"
                        inComment = True
                    else:
                        commentStart = "{"
                elif c == '\'':
                    if "'" == commentStart:
                        commentStart = "''"
                        inComment = True
                    else:
                        commentStart = "'"
            else:
                # Find comment end markers.
                if c == ']' and "[[" == commentStart:
                    if "]" == commentEnd:
                        commentEnd = ""
                        commentStart = ""
                        inComment = False
                    else:
                        commentEnd = "]"
                elif c == '}' and "{{" == commentStart:
                    if "}" == commentEnd:
                        commentEnd = ""
                        commentStart = ""
                        inComment = False
                    else:
                        commentEnd = "}"
                elif c == '\'' and "''" == commentStart:
                    if "'" == commentEnd:
                        commentEnd = ""
                        commentStart = ""
                        inComment = False
                    else:
                        commentEnd = "'"

            # Remove delimiters if in comment.
            if not inComment or c != '⁋':
                result += c

        return result

    def splitWordList(self, text):
        """ Splits the given text by comma, semicolon, line break, etc. and
            removes multiple types of special characters and affixes. The
            resulting segments are returned as a list of strings. """
        result = list()
        if text is None:
            return result

        t = text + "⁋"
        t = t.replace('\n', '⁋')
        t = re.sub(WordListProcessor.REFERENCE_PATTERN, "", t)
        t = re.sub(WordListProcessor.SUPERSCRIPT_PATTERN, "", t)  # TODO: Extract sense!
        t = re.sub(WordListProcessor.HTML_REMOVER, "", t)
        t = t.replace("&quot", "\"")
        t = t.replace(",", "⁋,")
        t = t.replace(";", "⁋")
        # print(t)
        # t = re.sub(WordListProcessor.BRACKETED_DELIMITER, "$1$2$3$4$5$6", t)
        # t = re.sub(WordListProcessor.ESCAPE_DELIMITER1, "$1$2", t)
        # t = re.sub(WordListProcessor.ESCAPE_DELIMITER2, "$1$2", t)
        # t = re.sub(WordListProcessor.ESCAPE_DELIMITER3, "$1$2", t)
        t = self.escapeDelimiters(t)
        # print(t)
        t = t.replace("⁋;", "⁋")
        t = t.replace("⁋,", "⁋")
        t = t.replace("]] or [[", "]]⁋[[")
        t = t.replace("]] and [[", "]]⁋[[")
        t = t.replace(" - ", "⁋")
        # t = t.replace(" / ", "⁋")
        j = t.find(" / ")  # Use ' / ' only as a delimiter if there are at least two of them!
        if j >= 0:
            j = t.find(" / ", j)
            if j >= 0:
                t = t.replace(" / ", "⁋")
                # print(t)

        # print(t)
        while True:
            delim = t.find('⁋')
            if delim >= 0:
                word = t[0:delim]
                if word:
                    # Normalize the word.
                    word = word.strip()
                    if word.lower().startswith("see also"):
                        word = word[8:].strip()
                    if word.lower().startswith("see"):
                        word = word[3:].strip()
                    if word.startswith(":"):
                        word = word[1:].strip()
                    word = self.deWikify(word).strip()
                    word = self.removeBrackets(word).strip()
                    word = self.removeTemplates(word).strip()
                    word = self.removeComments(word).strip()
                    if word.lower().startswith("see also"):
                        word = word[8:].strip()
                    if word.lower().startswith("see"):
                        word = word[3:].strip()
                    if word.startswith(":"):
                        word = word[1:].strip()
                    if word.endswith("."):
                        word = word[:-1].strip()
                    if word.endswith(","):
                        word = word[:-1].strip()

                    # Check for slashes.
                    word = word.replace(" / ", "/")
                    word = word.replace("/ ", "/")
                    i = word.find('/')
                    if word:
                        if i >= 0 and word.find(' ') < 0:
                            while True:
                                result.append(word[0:i])
                                word = word[i + 1:]
                                i = word.find('/')
                                if i < 0:
                                    break
                            result.append(word)
                        else:
                            result.append(word)

                t = t[delim + 1:]

            else:
                break

        return result

    # noinspection PyMethodMayBeStatic
    def deWikify(self, word):
        result = ""
        t = word
        while True:
            i = t.find("[[")
            if i >= 0:
                result += t[0: i]
                t = t[i + 2:]

                i = t.find("]]")
                if i >= 0:
                    wikifiedText = t[0: i]
                    t = t[i + 2:]

                    i = wikifiedText.find('|')
                    if i >= 0:
                        wikifiedText = wikifiedText[i + 1:]  # TODO: save link target.
                    result += wikifiedText

            else:
                break

        result += t
        return result

    # noinspection PyMethodMayBeStatic
    def removeBrackets(self, word):
        result = ""
        t = word
        while True:
            i = t.find("(")
            if i >= 0:
                result += t[:i]
                t = t[i+1:]

                i = t.find(")")
                if i >= 0:
                    # TODO: save bracketed comment!
                    t = t[i+1:]

            else:
                break

        result += t
        return result

    # noinspection PyMethodMayBeStatic
    def removeComments(self, word):
        result = ""
        t = word
        while True:
            i = t.find("''")
            if i >= 0:
                result += t[0:i]
                t = t[i+2:]

                i = t.find("''")
                if i >= 0:
                    # TODO: save bracketed comment!
                    t = t[i+2:]

            else:
                break

            result += t
        result += t
        return result

    # noinspection PyMethodMayBeStatic
    def removeTemplates(self, word):
        result = ""
        t = word
        while True:
            i = t.find("{{")
            if i >= 0:
                result += t[:i]
                t = t[i+2:]

                i = t.find("}}")
                if i >= 0:
                    templateText = t[:i]
                    t = t[i+2:]

                    # Process template
                    i = templateText.find('|')
                    if i >= 0:
                        templateName = templateText[:i]
                        # Link template
                        if "l" == templateName or templateName.startswith("l/"):
                            idx = templateText.find('|', i + 1)
                            if idx >= 0:
                                closing = templateText.find('|', idx + 1)
                                result += templateText[idx + 1: len(templateText) if closing == -1 else closing]
                            else:
                                result += templateText[i+1:]

            else:
                break

        result += t
        return result.strip()
