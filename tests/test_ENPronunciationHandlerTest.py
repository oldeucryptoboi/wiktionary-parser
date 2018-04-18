import unittest
from api.IPronunciation import IPronunciation
from api.entry import WiktionaryEntry, WiktionaryPage
from compat import *
from parser.en.components import ENEntryFactory, ENPronunciationHandler
from parser.util import ParsingContext
from tests import *


class ENPronunciationHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):
    """ Test case for {@link ENPronunciationHandler}. """

    def testDictionary(self):  # throws Exception {
        page = self.parse("dictionary.txt")
        pronunciations = page.getEntry(0).getPronunciations()
        iter_ = List(pronunciations).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈdɪkʃən(ə)ɹi/", "UK", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/\"dIkS@n(@)ri/", "UK", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈdɪkʃənɛɹi/", "North America", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/\"dIkS@nEri/", "North America", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-dictionary.ogg", "Audio (US)", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-uk-dictionary.ogg", "Audio (UK)", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testWomen(self):  # throws Exception {
        page = self.parse("women.txt")
        # self.printPronunciations(page)
        entryIter = List(page.getEntries()).iterator()
        pronIter = List(entryIter.next().getPronunciations()).iterator()

        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈwɪmɪn/", "RP", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈwɪmən/", "US", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-uk-women.ogg", "Audio (UK)", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.RHYME, "ɪmɪn", "", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        pronIter = List(entryIter.next().getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "zh-wǒmen.ogg", "audio", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "[ wo˨˩mən ]", "", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        self.assertFalse(entryIter.hasNext())

    def testBass(self):  # throws Exception {
        page = self.parse("bass.txt")
        # self.printPronunciations(page)
        entryIter = List(page.getEntries()).iterator()
        pronIter = List(entryIter.next().getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/beɪs/", "", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/beIs/", "", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-bass-low.ogg", "Audio (US)", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        pronIter = List(entryIter.next().getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/beɪs/", "", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/beIs/", "", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-bass-low.ogg", "Audio (US)", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        pronIter = List(entryIter.next().getPronunciations()).iterator()
        # self.assertPronunciation(PronunciationType.enPR, "/băs/", "", proniter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/bæs/", "", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/b{s/", "", pronIter.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-bass.ogg", "Audio (US)", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        self.assertIsNone(entryIter.next().getPronunciations())
        self.assertFalse(entryIter.hasNext())

    def testWord(self):  # throws Exception {
        page = self.parse("word.txt")
        # self.printPronunciations(page)
        entryIter = List(page.getEntries()).iterator()
        for i in range(3):
            pronIter = List(entryIter.next().getPronunciations()).iterator()
            self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/wɜːd/", "RP", pronIter.next())
            self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/w3:d/", "RP", pronIter.next())
            # self.assertPronunciation(IPronunciation.PronunciationType.IPA, "wûrd", "US", proniter.next()); #enPR
            self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/wɝd/", "US", pronIter.next())
            self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/w3`d/", "US", pronIter.next())
            self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-word.ogg", "Audio (US)", pronIter.next())
            self.assertPronunciation(IPronunciation.PronunciationType.RHYME, "ɜː(r)d", "", pronIter.next())
            self.assertFalse(pronIter.hasNext())

        pronIter = List(entryIter.next().getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "Nl-word.ogg", "audio", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        pronIter = List(entryIter.next().getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/word/", "", pronIter.next())
        self.assertFalse(pronIter.hasNext())
        self.assertFalse(entryIter.hasNext())

    def testWorker(self):
        w = ENPronunciationHandler()
        w.processHead("",  ParsingContext(None))
        w.processBody("* {{a|UK}} {{IPA|/ˈdɪkʃən(ə)ɹi/}}, {{SAMPA|/&quot;dIkS@n(@)ri/}}", None)
        w.processBody("* {{a|North America}} {{enPR|dĭk'shə-nĕr-ē}}, {{IPA|/ˈdɪkʃənɛɹi/}}, {{SAMPA|/&quot;dIkS@nEri/}}", None)
        w.processBody("* {{audio|en-us-dictionary.ogg|Audio (US)}}", None)
        w.processBody("* {{audio|en-uk-dictionary.ogg|Audio (UK)}}", None)

        w.processBody("* {{IPA|/fɹiː/}}, {{SAMPA|/fri:/}}", None)
        w.processBody("* {{audio|en-us-free.ogg|Audio (US)|lang=en}}", None)
        w.processBody("* {{audio|En-uk-free.ogg|Audio (UK)|lang=en}}", None)
        w.processBody("*: {{rhymes|iː}}", None)

        w.processBody("* {{a|RP}} {{IPA|/dɒɡ/}}, {{SAMPA|/dQg/}}", None)
        w.processBody("* {{a|US}} {{IPA|/dɔɡ/}}, {{SAMPA|/dOg/}}", None)
        w.processBody("* {{a|US, in accents with the [[cot-caught merger]]}} {{IPA|/dɑɡ/}}, {{SAMPA|/dAg/}}", None)
        w.processBody("* {{audio|en-us-dog.ogg|Audio (US)}}", None)
        w.processBody("* {{audio|En-uk-a dog.ogg|Audio (UK)}}", None)
        w.processBody("*: {{rhymes|ɒɡ}}", None)

        w.processBody("* {{IPA|lang=es|/pje/}}", None)

        w.processBody("* {{IPA|/ɑː/|/a/|lang=mul}} {{qualifier|most languages}}", None)

        w.processBody("* {{qualifier|letter name}}", None)
        w.processBody("** {{a|RP|GenAm}} {{IPA|/eɪ̯/}}, {{SAMPA|/eI/}}", None)
        w.processBody("** {{audio|en-us-a.ogg|Audio (US)}}", None)
        w.processBody("** {{a|AusE}} {{IPA|/æɪ/}}, {{SAMPA|/{I/}}", None)
        w.processBody("* {{rhymes|eɪ}}", None)
        w.processBody(
            "*: The current pronunciation is a comparatively modern sound, and has taken the place of what, till about the early part of the 15th century, was similar to that in other languages.",
            None)

        w.processBody("* {{sense|letter name}} {{IPA|/a/|lang=eo}}", None)
        w.processBody("* {{sense|phoneme}} {{IPA|/a/|lang=eo}}", None)

        iter_ = List(w.getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈdɪkʃən(ə)ɹi/", "UK", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/&quot;dIkS@n(@)ri/", "UK", iter_.next())
        # self.assertPronunciation(IPronunciation.PronunciationType.IPA, "dĭk'shə-nĕr-ē", "North America", iter_.next()); #enPR
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈdɪkʃənɛɹi/", "North America", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/&quot;dIkS@nEri/", "North America", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-dictionary.ogg", "Audio (US)", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-uk-dictionary.ogg", "Audio (UK)", iter_.next())

        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/fɹiː/", "", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/fri:/", "", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-free.ogg", "Audio (US)", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "En-uk-free.ogg", "Audio (UK)", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.RHYME, "iː", "", iter_.next())

        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/dɒɡ/", "RP", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/dQg/", "RP", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/dɔɡ/", "US", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/dOg/", "US", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/dɑɡ/", "US, in accents with the [[cot-caught merger]]",
                                 iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/dAg/", "US, in accents with the [[cot-caught merger]]",
                                 iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-dog.ogg", "Audio (US)", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "En-uk-a dog.ogg", "Audio (UK)", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.RHYME, "ɒɡ", "", iter_.next())

        # TODO: Pronunciation cannot be extracted properly yet.
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/pje/", "", iter_.next())
        iter_.next()  # self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ɑː/", "{{qualifier|most languages}}", iter_.next())
        iter_.next()  # self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/eɪ̯/", "RP|GenAm {{qualifier|letter name}}", iter_.next())
        iter_.next()  # self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/eI/", "RP|GenAm {{qualifier|letter name}}", iter_.next())
        iter_.next()  # self.assertPronunciation(IPronunciation.PronunciationType.AUDIO, "en-us-a.ogg", "Audio (US) {{qualifier|letter name}}", iter_.next())
        iter_.next()  # self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/æɪ/", "AusE {{qualifier|letter name}}", iter_.next())
        iter_.next()  # self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/{I/", "AusE {{qualifier|letter name}}", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.SAMPA, "/{I/", "AusE", iter_.next())
        self.assertPronunciation(IPronunciation.PronunciationType.RHYME, "eɪ", "", iter_.next())

        iter_.next()  # assertPronunciation(IPronunciation.PronunciationType.IPA, "/a/", "{{sense|letter name}}", iter_.next())
        iter_.next()  # assertPronunciation(IPronunciation.PronunciationType.IPA, "/a/", "{{sense|phoneme}} ", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testFlippedLanguageParameter(self):
        w = ENPronunciationHandler()
        w.processHead("", ParsingContext(None))
        w.processBody("* {{a|Brazil}} {{IPA|lang=pt|/ˈfa.siw/}}", None)
        iter_ = List(w.getPronunciations()).iterator()
        self.assertPronunciation(IPronunciation.PronunciationType.IPA, "/ˈfa.siw/", "Brazil", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testRawPronunciationType(self):
        pronunciations = self.process("* {{IPA|/budɛ̃/|lang=fr}}", "* {{fr-IPA|cauboille}}", "* {{zh-pron}}")
        self.assertEqual(3, len(pronunciations))

        self.assertEqual("/budɛ̃/", pronunciations[0].getText())
        self.assertEqual(IPronunciation.PronunciationType.IPA, pronunciations[0].getType())

        self.assertEqual("{{fr-IPA|cauboille}}", pronunciations[1].getText())
        self.assertEqual(IPronunciation.PronunciationType.RAW, pronunciations[1].getType())

        self.assertEqual("{{zh-pron}}", pronunciations[2].getText())
        self.assertEqual(IPronunciation.PronunciationType.RAW, pronunciations[2].getType())

    def testFiltersEmptyPronunciations(self):
        pronunciations = self.process("* {{IPA|/ma.dam wa.ta.na.be/||lang=fr}}")
        self.assertEqual(1, len(pronunciations))
        self.assertEqual("/ma.dam wa.ta.na.be/", pronunciations[0].getText())

    def assertPronunciation(self, type, text, note, actual):
            self.assertEqual(type, actual.getType(), "type does not match")
            self.assertEqual(text, actual.getText(), "text does not match")
            self.assertEqual(note, actual.getNote(), "note does not match")

    def process(self, *body):
        entry = WiktionaryEntry()

        # noinspection PyUnusedLocal
        def findEntry(self, _):
            return entry

        entryFactory = type("_ENEntryFactory", (ENEntryFactory,), {"findEntry": findEntry})
        context = ParsingContext(WiktionaryPage(), entryFactory())

        handler = ENPronunciationHandler()
        handler.processHead("testing", context)
        for line in body:
            handler.processBody(line, context)

        return handler.getPronunciations()
