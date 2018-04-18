from compat import Logger
from api.util.GrammaticalPerson import GrammaticalPerson
from api.util.GrammaticalNumber import GrammaticalNumber
from api.util.GrammaticalTense import GrammaticalTense
from api.util.GrammaticalDegree import GrammaticalDegree
from api.util.NonFiniteForm import NonFiniteForm
from api.entry.WiktionaryWordForm import WiktionaryWordForm
from api.util import TemplateParser

from parser.en.components.IWordFormHandler import IWordFormHandler
from parser.en.components.IHeadwordLineHandler import IHeadwordLineHandler


class ENWordFormHandler(TemplateParser.ITemplateHandler, IWordFormHandler, IHeadwordLineHandler):
    """ Parser component for extracting inflected word forms from
        the English Wiktionary. """

    logger = Logger.getLogger("ENWordFormHandler")

    def __init__(self, lemma):
        """ Initializes the handler for the specified lemma. The lemma is
         *  required since the inflection templates often defines only affixed
         *  that are to be added to the lemma. """
        self.lemma = lemma
        self.wordForms = list()

        self.rawHeadwordLine = None

    def handle(self, template):
        if "en-noun" == template.getName():
            self.handleNounTemplate(template)
        elif "en-proper noun" == template.getName():
            self.handleProperNounTemplate(template)
        elif "en-verb" == template.getName():
            self.handleVerbTemplate(template)
        elif "en-adj" == template.getName():
            self.handleAdjectiveTemplate(template)
        
        return None

    def handleNounTemplate(self, template):
        hasPlural, addAll = False, False
        for key, value in template.getNamedParams():
            if key.startswith("pl"):
                self.wordForms.append(self.createPlural(None, value))
                hasPlural = True

        # http://en.wiktionary.org/wiki/Template:en-noun
        if template.getNumberedParamsCount() == 0:
            if not hasPlural:
                self.wordForms.append(self.createPlural(self.lemma, "s"))
        elif template.getNumberedParamsCount() == 1:
            param1 = template.getNumberedParam(0)
            if "-" == param1:
                self.wordForms.append(self.createPlural(None, None))  # uncountable
            elif "~" == param1:
                self.wordForms.append(self.createPlural(self.lemma, "s"))  # countable and uncountable
            elif "!" == param1:
                self.logger.finer("Not attested word form: " + template)  # not attested
            elif "?" == param1:
                self.logger.finer("Unknown word form: " + template)  # unknown
            else:
                self.wordForms.append(self.createPlural(self.lemma, param1))
        elif template.getNumberedParamsCount() == 2:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            if "-" == param1:
                self.wordForms.append(self.createPlural(self.lemma, param2))  # usually uncountable
            elif "-" == param2:
                self.wordForms.append(self.createPlural(self.lemma, param1))  # countable and uncountable
            elif "!" == param1:
                self.logger.finer("Not attested word form: " + template)  # not attested
            elif "?" == param1:
                self.logger.finer("Unknown word form: " + template)  # unknown
            elif "?" == param2:
                self.wordForms.append(self.createPlural(self.lemma, param1))  # unknown
            elif "ies" == param2:
                self.wordForms.append(self.createPlural(None, param1 + param2))  # unknown
            else:
                addAll = True
        
        if addAll or template.getNumberedParamsCount() > 2:
            length = template.getNumberedParamsCount()
            inserted = False
            for i in range(length):
                param = template.getNumberedParam(i)
                if param is None or "~" == param:
                    continue

                if "s" == param or "es" == param:
                    self.wordForms.append(self.createPlural(self.lemma, param))
                elif "" == param:
                    if not inserted:
                        self.wordForms.append(self.createPlural(self.lemma, "s"))
                else:
                    self.wordForms.append(self.createPlural(None, param))
                inserted = True
            
    def handleProperNounTemplate(self, template):
        # http://en.wiktionary.org/wiki/Template:en-noun
        if template.getNumberedParamsCount() == 0:
            self.wordForms.append(self.createPlural(None, None))  # uncountable
        elif template.getNumberedParamsCount() == 1:
            param1 = template.getNumberedParam(0)
            self.wordForms.append(self.createPlural(self.lemma, param1))
        elif template.getNumberedParamsCount() == 2:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            if "-" == param1:
                self.wordForms.append(self.createPlural(self.lemma, param2))  # usually uncountable
            elif "-" == param2:
                self.wordForms.append(self.createPlural(self.lemma, param1))  # countable and uncountable
            elif "!" == param1:
                self.logger.finer("Not attested word form: " + template)  # not attested
            elif "?" == param1:
                self.logger.finer("Unknown word form: " + template)  # unknown
            elif "?" == param2:
                self.wordForms.append(self.createPlural(self.lemma, param1))  # unknown
            else:
                self.wordForms.append(self.createPlural(None, param1 + param2))  # unknown
        
        for key, value in template.getNamedParams():
            if key.startswith("pl"):
                self.wordForms.append(self.createPlural(None, value))
    
    def handleVerbTemplate(self, template):
        # http://en.wiktionary.org/wiki/Template:en-verb
        if template.getNumberedParamsCount() == 0:
            self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
            self.wordForms.append(self.createFormPresentParticiple(self.lemma + "ing"))
            self.wordForms.append(self.createFormSimplePast(self.lemma + "ed"))
            self.wordForms.append(self.createFormPastParticiple(self.lemma + "ed"))
        elif template.getNumberedParamsCount() == 1:
            param1 = template.getNumberedParam(0)
            if "d" == param1:
                self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
                self.wordForms.append(self.createFormPresentParticiple(self.lemma + "ing"))
                self.wordForms.append(self.createFormSimplePast(self.lemma + "d"))
                self.wordForms.append(self.createFormPastParticiple(self.lemma + "d"))
            elif "es" == param1:
                self.wordForms.append(self.createFormThirdPerson(self.lemma + "es"))
                self.wordForms.append(self.createFormPresentParticiple(self.lemma + "ing"))
                self.wordForms.append(self.createFormSimplePast(self.lemma + "ed"))
                self.wordForms.append(self.createFormPastParticiple(self.lemma + "ed"))
            else:
                self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + "ed"))
                self.wordForms.append(self.createFormPastParticiple(param1 + "ed"))
            
        elif template.getNumberedParamsCount() == 2:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            if "es" == param2:
                self.wordForms.append(self.createFormThirdPerson(param1 + "es"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + "ed"))
                self.wordForms.append(self.createFormPastParticiple(param1 + "ed"))
            elif "ies" == param2:
                self.wordForms.append(self.createFormThirdPerson(param1 + "ies"))
                self.wordForms.append(self.createFormPresentParticiple(self.lemma + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + "ied"))
                self.wordForms.append(self.createFormPastParticiple(param1 + "ied"))
            elif "d" == param2:
                self.wordForms.append(self.createFormThirdPerson(param1 + "s"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + "d"))
                self.wordForms.append(self.createFormPastParticiple(param1 + "d"))
            elif "ing" == param2:
                self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + "ing"))
                self.wordForms.append(self.createFormSimplePast(self.lemma + "d"))
                self.wordForms.append(self.createFormPastParticiple(self.lemma + "d"))
            
        elif template.getNumberedParamsCount() == 3:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            param3 = template.getNumberedParam(2)
            if "es" == param3:
                self.wordForms.append(self.createFormThirdPerson(param1 + param2 + "es"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + param2 + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + param2 + "ed"))
                self.wordForms.append(self.createFormPastParticiple(param1 + param2 + "ed"))
            elif "ed" == param3 and "i" == param2:
                self.wordForms.append(self.createFormThirdPerson(param1 + param2 + "es"))
                self.wordForms.append(self.createFormPresentParticiple(self.lemma + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + param2 + "ed"))
                self.wordForms.append(self.createFormPastParticiple(param1 + param2 + "ed"))
            elif "ed" == param3:
                self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + param2 + "ing"))
                self.wordForms.append(self.createFormSimplePast(param1 + param2 + "ed"))
                self.wordForms.append(self.createFormPastParticiple(param1 + param2 + "ed"))
            elif "ing" == param3:
                self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
                self.wordForms.append(self.createFormPresentParticiple(param1 + param2 + "ing"))
                self.wordForms.append(self.createFormSimplePast(self.lemma + "d"))
                self.wordForms.append(self.createFormPastParticiple(self.lemma + "d"))
            else:
                if "" == param1:
                    self.wordForms.append(self.createFormThirdPerson(self.lemma + "s"))
                else:
                    self.wordForms.append(self.createFormThirdPerson(param1))
                self.wordForms.append(self.createFormPresentParticiple(param2))
                self.wordForms.append(self.createFormSimplePast(param3))
                self.wordForms.append(self.createFormPastParticiple(param3))
            
        elif template.getNumberedParamsCount() == 4:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            param3 = template.getNumberedParam(2)
            param4 = template.getNumberedParam(3)
            self.wordForms.append(self.createFormThirdPerson(param1))
            self.wordForms.append(self.createFormPresentParticiple(param2))
            self.wordForms.append(self.createFormSimplePast(param3))
            self.wordForms.append(self.createFormPastParticiple(param4))
        
        for key, value in template.getNamedParams():
            if key.startswith("pres"):
                self.wordForms.append(self.createFormPresentParticiple(value))
            elif key == "past2":
                length = template.getNumberedParamsCount()
                if length == 3:
                    self.wordForms.append(self.createFormSimplePast(value))
                    self.wordForms.append(self.createFormPastParticiple(value))
                else:
                    self.wordForms.append(self.createFormSimplePast(value))

    # noinspection PyMethodMayBeStatic
    def removeEndingE(self, str_):
        # remove the ending letter 'e' if exists
        return str_[:-1] if str_.endswith("e") else str

    def handleAdjectiveTemplate(self, template):
        # http://en.wiktionary.org/wiki/Template:en-adj
        if template.getNumberedParamsCount() == 0:
            self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
            self.wordForms.append(self.createAdjectiveForm("more " + self.lemma, GrammaticalDegree.COMPARATIVE))
            self.wordForms.append(self.createAdjectiveForm("most " + self.lemma, GrammaticalDegree.SUPERLATIVE))
        elif template.getNumberedParamsCount() == 1:
            param1 = template.getNumberedParam(0)
            if "er" == param1:
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(self.lemma) + "er", GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(self.lemma) + "est", GrammaticalDegree.SUPERLATIVE))
            elif "-" == param1:  # not comparable
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                self.wordForms.append(self.createAdjectiveForm(None, GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm(None, GrammaticalDegree.SUPERLATIVE))
            elif "?" == param1:
                self.logger.finer("Unknown word form: " + template)  # unknown
            else:
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                if "" == param1:
                    self.wordForms.append(self.createAdjectiveForm("more " + self.lemma, GrammaticalDegree.COMPARATIVE))
                else:
                    self.wordForms.append(self.createAdjectiveForm(param1, GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm("most " + self.lemma, GrammaticalDegree.SUPERLATIVE))
            
        elif template.getNumberedParamsCount() == 2:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            if "er" == param2:
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(param1) + "er", GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(param1) + "est", GrammaticalDegree.SUPERLATIVE))
            elif "er" == param1 and "more" == param2:
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(self.lemma) + "er", GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm("more " + self.lemma, GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(self.lemma) + "est", GrammaticalDegree.SUPERLATIVE))
                self.wordForms.append(self.createAdjectiveForm("most " + self.lemma, GrammaticalDegree.SUPERLATIVE))
            elif "-" == param1:  # not generally comparable
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                self.wordForms.append(self.createAdjectiveForm(param2, GrammaticalDegree.COMPARATIVE))
                if "-" == param2:
                    self.wordForms.append(self.createAdjectiveForm(param2, GrammaticalDegree.SUPERLATIVE))
                else:
                    self.wordForms.append(self.createAdjectiveForm("most " + self.lemma, GrammaticalDegree.SUPERLATIVE))
            else:
                self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                self.wordForms.append(self.createAdjectiveForm(param1, GrammaticalDegree.COMPARATIVE))
                self.wordForms.append(self.createAdjectiveForm(param2, GrammaticalDegree.SUPERLATIVE))
            
        elif template.getNumberedParamsCount() == 3:
            param1 = template.getNumberedParam(0)
            param2 = template.getNumberedParam(1)
            param3 = template.getNumberedParam(2)
            if "-" == param1:
                if "er" == param3:
                    self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                    self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(param2) + "er", GrammaticalDegree.COMPARATIVE))
                    self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(param2) + "est", GrammaticalDegree.SUPERLATIVE))
                elif "er" == param2 and "more" == param3:
                    self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                    self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(self.lemma) + "er", GrammaticalDegree.COMPARATIVE))
                    self.wordForms.append(self.createAdjectiveForm("more " + self.lemma, GrammaticalDegree.COMPARATIVE))
                    self.wordForms.append(self.createAdjectiveForm(self.removeEndingE(self.lemma) + "est", GrammaticalDegree.SUPERLATIVE))
                    self.wordForms.append(self.createAdjectiveForm("most " + self.lemma, GrammaticalDegree.SUPERLATIVE))
                else:
                    self.wordForms.append(self.createAdjectiveForm(self.lemma, GrammaticalDegree.POSITIVE))
                    self.wordForms.append(self.createAdjectiveForm(param2, GrammaticalDegree.COMPARATIVE))
                    self.wordForms.append(self.createAdjectiveForm(param3, GrammaticalDegree.SUPERLATIVE))

    # noinspection PyMethodMayBeStatic
    def createWordForm(self, wordForm):
        if wordForm is not None:
            wordForm = wordForm.strip()
            if "-" == wordForm:
                wordForm = None
        
        result = WiktionaryWordForm(wordForm)
        return result
    
    def createPlural(self, wordForm, pluralParam):
        if "s" == pluralParam or "es" == pluralParam:
            wordForm = wordForm + pluralParam
        else:
            wordForm = pluralParam
        result = self.createWordForm(wordForm)
        result.setNumber(GrammaticalNumber.PLURAL)
        return result
    
    def createFormThirdPerson(self, wordForm):
        result = self.createWordForm(wordForm)
        result.setPerson(GrammaticalPerson.THIRD)
        result.setNumber(GrammaticalNumber.SINGULAR)
        result.setTense(GrammaticalTense.PRESENT)
        return result
    
    def createFormPresentParticiple(self, wordForm):
        result = self.createWordForm(wordForm)
        result.setNonFiniteForm(NonFiniteForm.PARTICIPLE)
        result.setTense(GrammaticalTense.PRESENT)
        return result
    
    def createFormSimplePast(self, wordForm):
        result = self.createWordForm(wordForm)
        result.setTense(GrammaticalTense.PAST)
        return result

    def createFormPastParticiple(self, wordForm):
        result = self.createWordForm(wordForm)
        result.setNonFiniteForm(NonFiniteForm.PARTICIPLE)
        result.setTense(GrammaticalTense.PAST)
        return result
    
    def createAdjectiveForm(self, wordForm, degree):
        result = self.createWordForm(wordForm)
        result.setDegree(degree)
        return result
    
    def parse(self, line):
        if self.rawHeadwordLine is not None:
            return False  # already done
        elif line.startswith("{{en-"):
            self.rawHeadwordLine = line
            TemplateParser.parse(line, self)
            return True
        elif self.isHeadwordLine(line):
            self.rawHeadwordLine = line
            return True
        else:
            return False
        
    def getWordForms(self):
        return self.wordForms

    def getGenders(self):
        return None

    def getRawHeadwordLine(self):
        return self.rawHeadwordLine
