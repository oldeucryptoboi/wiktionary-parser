from .Language import Language
from collections import OrderedDict


class TemplateParser:
    """ Static helper class for parsing wiki markup text that contains templates.
        The template parser identifies templates in the given wiki text and
        replaces them as specified by a :@link ITemplateHandler. """

    class Template:
        """ A template is a reusable pattern that can be added to any wiki page. The
            template is being substituted by its definition upon rendering the wiki
            page to HTML. A template has a unique name. It can be equipped with
            multiple parameters. The parameters are divided into numbered and named
            parameters. The former are indexed by integers (starting with 0) the
            latter are key-value pairs. """

        def __init__(self, name):
            # Creates a new template with the given name.
            self.name = name
            self.namedParams = OrderedDict()
            self.numberedParams = list()

        def getName(self):
            # Returns the name of the template.
            return self.name

        def addParam(self, value):
            self.numberedParams.append(value)

        def addNamedParam(self, key, value):
            # Add a named parameter with the given key and value.
            if key in self.namedParams:
                suffix = 2
                while (key + suffix) in self.namedParams:
                    suffix += 1

                self.namedParams[key + suffix] = value
            else:
                self.namedParams[key] = value

        def getNumberedParam(self, idx):
            """ Return the numbered parameter with the given index or <code>None/<code>
                if no such parameter exists. """
            return self.numberedParams[idx]

        def getNamedParam(self, key):
            """ Return the named parameter with the given key or <code>None/<code>
                if no such parameter exists. """
            return self.namedParams.get(key)

        def getNumberedParams(self):
            """ Iterate over all numbered parameters. """
            return self.numberedParams

        def getNamedParams(self):
            """ Iterate over all named parameters. """
            return self.namedParams.items()

        def getParamsCount(self):
            """ Returns the number of all parameters (including numbered and named
                parameters). """
            return len(self.numberedParams) + len(self.namedParams)

        def getNumberedParamsCount(self):
            """ Returns number of all numbered parameters. """
            return len(self.numberedParams)

        def getNamedParamsCount(self):
            """ Returns number of all named parameters. """
            return len(self.namedParams)

    class ITemplateHandler:
        """ Interface that is expected by the :@link TemplateParser. The template
            parser invokes an implementation of this interface to decide what is
            to be done with a template. """

        def handle(self, template):
            """ Invoked by the :@link TemplateParser for every template that occurs
                in a text. The parser replaces the template by the result of this
                method. If <code>None</code> is returned, no substitution is made,
                but the original template string remains in the text. """
            pass

    class EtymologyTemplateHandler(ITemplateHandler):
        # Implementation of an :@link ITemplateHandler for parsing etymology
        # information in Wiktionary.

        def handle(self, template):
            if template.getName() == "etyl":
                languageCode = template.getNumberedParam(0)
                language = Language.findByCode(languageCode)
                if language is None:
                    return "{" + languageCode + "}"
                else:
                    return language.getName()

            elif template.getName() == "term":
                term = template.getNumberedParam(0)
                if template.getNumberedParamsCount() >= 3:
                    return term + " (“" + template.getNumberedParam(2) + "”)"
                else:
                    return term

            elif template.getName() == "recons":
                term = template.getNumberedParam(0)
                if template.getNumberedParamsCount() >= 3:
                    return "*" + term + " (“" + template.getNumberedParam(2) + "”)"
                else:
                    return "*" + term

            # Remove other templates.
            return ""

    @classmethod
    def parse(cls, wikiText, handler):
        """ Parse the given wiki text and substitute each template in the text
            using the specified template handler. """
        result = ""
        text = wikiText
        while True:
            startIdx = text.find("{{")
            if startIdx >= 0:
                result += text[:startIdx]
                endIdx = text.find("}}", startIdx)
                if endIdx >= 0:
                    handled = False
                    templateText = text[startIdx + 2:endIdx]
                    if handler is not None:
                        template = TemplateParser.parseTemplate(templateText)
                        if template is not None:
                            replacement = handler.handle(template)
                            if replacement is not None:
                                result += replacement
                                handled = True

                    if not handled:
                        result += "{{" + templateText + "}}"
                    text = text[endIdx + 2:]
                else:
                    text = text[startIdx + 2:]

            else:
                break

        result += text

        return result

    @classmethod
    def parseTemplate(cls, templateText):
        """ Creates a :@link Template from the given text. That is, the
            template's name and parameters are extracted from the text and
            stored in the template instance. """

        # Split the template text to access the parameters.
        params = templateText.split('|')
        if not params:
            return None

        result = TemplateParser.Template(params[0])
        idx = -1
        for param in params:
            # Skip the template name.
            if idx < 0:
                idx += 1
                continue

            # Check for named params.
            j = param.find('=')
            if j >= 0:
                key = param[:j]
                value = param[j + 1:]
                result.addNamedParam(key, value)
            else:
                result.addParam(param)

        return result
