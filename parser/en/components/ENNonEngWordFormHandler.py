import re
from api.util import TemplateParser
from parser.en.components.IWordFormHandler import IWordFormHandler
from parser.en.components.IHeadwordLineHandler import IHeadwordLineHandler
from api.util.GrammaticalGender import GrammaticalGender


class ENNonEngWordFormHandler(IWordFormHandler, IHeadwordLineHandler, TemplateParser.ITemplateHandler):
    """ Support for parsing word forms for non-English entries in the English Wiktionary. """

    HEAD_PATTERN = re.compile("\\A\\{\\{head\\|")  
    NOUN_PATTERN = re.compile("\\A\\{\\{(\\w+)\\-noun")  

    def __init__(self):
        self.rawHeadwordLine = None
        self.genders = None

    def parse(self, line):
        if self.rawHeadwordLine is not None:
            return False  # already done

        elif self.canExtractGenderInformation(line):
            self.rawHeadwordLine = line
            self.genders = list()
            TemplateParser.parse(line, self)
            return True
        elif self.isHeadwordLine(line):
            self.rawHeadwordLine = line
            return True
        else:
            return False

    def getWordForms(self):
        return list()
    
    def getGenders(self):
        return self.genders
    
    def getRawHeadwordLine(self):
        return self.rawHeadwordLine

    def handle(self, template):
        if template.getName() == "la-noun":
            self.handleLatinNounTemplate(template)
        elif template.getName().endswith("-noun"):
            self.handleGenericNounTemplate(template)
        elif template.getName() == "g":
            self.handleGenericNounTemplate(template)
        elif template.getName() == "head":
            self.handleHeadwordTemplate(template)
        
        return None
    
    # pt-noun: m, f, mf, m-f, m-p, f-p, m-f-p, morf (deprecated in favour of m|g2=f), and ?. g2=The second gender, to be used when different people use the same word with different genders
    # fr-noun: m, f, m-p or f-p. It also accepts mf as a shortcut for m|g2=f. g2= The second gender, if any.
    # es-noun: m, f, m-p, f-p or mf
    # de-noun: Use m, f, n for neuter. To specify more than one gender, use g2= or g3=
    def handleGenericNounTemplate(self, template):
        if template.getNumberedParamsCount() > 0:
            genderParam = template.getNumberedParam(0)
            self.extractGender(genderParam)
        
    # g= and g2=, g3=...
    # m, m-p, m-an-p, f-d, m-p, m-p etc.
    def handleHeadwordTemplate(self, template):
        genderParam = template.getNamedParam("g")
        self.extractGender(genderParam)

    # la-noun: ::la-noun|casa|casae|casae|f|first
    def handleLatinNounTemplate(self, template):
        if template.getNumberedParamsCount() >= 4:
            self.extractGender(template.getNumberedParam(3))
        
    def extractGender(self, genderParam):
        if genderParam is None:
            return

        # TODO: properly parse gender combinations
        gender = None
        if "m" == genderParam or genderParam.startswith("m"):
            gender = GrammaticalGender.MASCULINE
        elif "f" == genderParam or genderParam.startswith("f"):
            gender = GrammaticalGender.FEMININE
        elif "n" == genderParam:
            gender = GrammaticalGender.NEUTER

        if gender is not None:
            self.genders.append(gender)

    @classmethod
    def canExtractGenderInformation(cls, line):
        return re.search(ENNonEngWordFormHandler.HEAD_PATTERN, line) is not None or re.search(ENNonEngWordFormHandler.NOUN_PATTERN, line) is not None
