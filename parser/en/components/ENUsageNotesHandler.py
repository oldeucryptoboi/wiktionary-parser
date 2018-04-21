from parser.en.components.ENBlockHandler import ENBlockHandler
from errors import RuntimeException
from api.entry import WikiString


class ENUsageNotesHandler(ENBlockHandler):

    def __init__(self):
        super().__init__("Usage notes")
        self.usageNotes = None

    def processHead(self, text, context):
        self.usageNotes = ""
        return super().processHead(text, context)
    
    def processBody(self, textLine, context):
        textLine = textLine.strip()
        if textLine:
            self.usageNotes += textLine + "\n"
        
        return super().processBody(textLine, context)

    def fillContent(self, context):
        if self.usageNotes:
            entry = context.findEntry()
            if entry is None:
                raise RuntimeException("entry is None")
            
            entry.setUsageNotes(WikiString(self.usageNotes.strip()))
        
        super().fillContent(context)
