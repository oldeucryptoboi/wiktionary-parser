import re


# noinspection PyMethodMayBeStatic
class IHeadwordLineHandler:

    LEGACY_PATTERN = re.compile("\\A'''[^']+'''")

    def isTemplate(self, line):
        return line.startswith("{{")
    
    def isExcludedTemplate(self, line):
        return any(line.lower().find(template) >= 0 for template in ["{{wikipedia", "{{slim-wikipedia", "{{wiki", "{{wikispecies", "{{wikiversity", "{{wikiquote", "{{commons", "{{attention", "{{rfc", "{{examples", "{{enum|", "{{no entry"])

    def isLegacyHeader(self, line):
        return re.search(IHeadwordLineHandler.LEGACY_PATTERN, line) is not None
    
    def isHeadwordLine(self, line):
        return self.isLegacyHeader(line) or (self.isTemplate(line) and not self.isExcludedTemplate(line))
