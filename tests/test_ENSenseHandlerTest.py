import unittest

from api import RelationType
from api.entry import WiktionaryPage
from api.util.GrammaticalGender import GrammaticalGender
from compat import List
from parser.en.components import ENSenseHandler
from parser.util import ParsingContext
from tests import *


class ENSenseHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):

    def testHead(self):  # throws Exception
        page = self.parse("head.txt")
        senseIter = List(page.getEntry(0).getSenses()).iterator()
        self.assertEqual(
            "{{countable}} The part of the [[body]] of an animal or human which contains the [[brain]], [[mouth]]{{,}} and main [[sense]] [[organs]].",
            senseIter.next().getGloss().getText())
        self.assertEqual("{{uncountable}} [[mental|Mental]] or [[emotional]] [[aptitude]] or [[skill]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{countable}} [[mind|Mind]]; one's own [[thought]]s.", senseIter.next().getGloss().getText())
        self.assertEqual("{{countable}} The [[topmost]], [[foremost]], or [[leading]] part.",
                         senseIter.next().getGloss().getText())
        self.assertEqual(
            "The end of a rectangular [[table]] furthest from the entrance; traditionally considered a seat of honor.",
            senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{billiards}} The end of a [[pool]] table opposite the end where the balls have been [[rack]]ed.",
            senseIter.next().getGloss().getText())
        self.assertEqual("{{countable}} The [[principal]] [[operative]] part of a machine."
                         + "\nThe end of a [[hammer]], [[axe]], {{soplink|golf|club}}{{,}} or similar [[implement]] used for striking other objects."
                         + "\nThe end of a [[nail]], [[screw]], [[bolt]]{{,}} or similar [[fastener]] which is opposite the [[point]]; usually [[blunt]] and relatively [[wide]]."
                         + "\nThe [[sharp]] end of an [[arrow]], [[spear]]{{,}} or [[pointer]]."
                         + "\n{{lacrosse}} The top part of a [[lacrosse stick]] that holds the [[ball]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("The [[source]] of a [[river]]; the end of a [[lake]] where a river flows into it.",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{rfc-sense}} The front, as of a [[queue]].", senseIter.next().getGloss().getText())
        self.assertEqual("[[headway|Headway]]; [[progress]].", senseIter.next().getGloss().getText())
        self.assertEqual("The foam that forms on top of [[beer]] or other carbonated [[beverage]]s.",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{countable}} [[leader|Leader]]; [[chief]]; [[mastermind]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("A [[headmaster]] or [[headmistress]].", senseIter.next().getGloss().getText())
        self.assertEqual("A [[headache]]; especially one resulting from [[intoxication]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("A clump of [[leave]]s or [[flower]]s; a [[capitulum]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{anatomy}} The rounded part of a bone fitting into a depression in another bone to form a ball-and-socket [[joint]].",
            senseIter.next().getGloss().getText())
        self.assertEqual("An individual [[person]].", senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{uncountable|[[w:Measure word|measure word]] for [[livestock]] and [[game]]}} A single [[animal]].",
            senseIter.next().getGloss().getText())
        self.assertEqual("The population of [[game]].", senseIter.next().getGloss().getText())
        self.assertEqual("Topic; [[subject]].", senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{linguistics}} A [[morpheme]] that determines the category of a [[compound]] or the word that determines the [[syntactic]] type of the [[phrase]] of which it is a member.",
            senseIter.next().getGloss().getText())
        self.assertEqual("{{jazz}} The principal [[melody]] or [[theme]] of a piece.",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{British|geology}} Deposits near the top of a [[geological]] [[succession]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{medicine}} The end of an [[abscess]] where [[pus]] collects.",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{uncountable}} [[denouement]]; [[crisis]]", senseIter.next().getGloss().getText())
        self.assertEqual(
            "A [[machine]] element which reads or writes [[electromagnetic]] signals to or from a storage medium.",
            senseIter.next().getGloss().getText())
        self.assertEqual("{{music}} The [[headstock]] of a [[guitar]].", senseIter.next().getGloss().getText())
        self.assertEqual("{{music}} A [[drum head]], the [[membrane]] which is hit to produce [[sound]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{engineering}} The end cap of a cylindrically-shaped [[pressure vessel]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{automotive}} The [[cylinder head]], a platform above the [[cylinder]]s in an [[internal combustion engine]], containing the [[valve]]s and [[spark plug]]s.",
            senseIter.next().getGloss().getText())
        self.assertEqual("A buildup of [[fluid]] [[pressure]], often quantified as [[pressure head]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{fluid dynamics}} The difference in [[elevation]] between two points in a [[column]] of fluid, and the resulting [[pressure]] of the fluid at the lower point.",
            senseIter.next().getGloss().getText())
        self.assertEqual("{{fluid dynamics}} More generally, [[energy]] in a mass of fluid divided by its [[weight]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{nautical}} The [[top]] edge of a [[sail]].", senseIter.next().getGloss().getText())
        self.assertEqual("{{nautical}} The [[bow]] of a nautical vessel.", senseIter.next().getGloss().getText())
        self.assertEqual("{{nautical}} The [[toilet]] of a [[ship]].", senseIter.next().getGloss().getText())
        self.assertEqual("{{uncountable|slang}} [[fellatio|Fellatio]] or [[cunnilingus]]; [[oral sex]].",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{slang}} The [[glans penis]].", senseIter.next().getGloss().getText())
        self.assertEqual("{{countable|slang}} A heavy or [[habitual]] user of [[illicit]] [[drug]]s.",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{British}} A [[headland]].", senseIter.next().getGloss().getText())
        self.assertFalse(senseIter.hasNext())

    def testForGoodMeasure(self):  # throws Exception
        page = self.parse("for_good_measure.txt")
        senseIter = List(page.getEntry(0).getSenses()).iterator()
        self.assertEqual("{{idiomatic}} In excess of the minimum required; Added as an [[extra]]",
                         senseIter.next().getGloss().getText())
        self.assertFalse(senseIter.hasNext())

    def testBatsman(self):  # throws Exception
        page = self.parse("batsman.txt")
        senseIter = List(page.getEntry(0).getSenses()).iterator()
        self.assertEqual("{{cricket}} A [[player]] of the [[batting]] [[side]] now on the [[field]]",
                         senseIter.next().getGloss().getText())
        self.assertEqual("{{cricket}} The [[player]] now [[receiving]] [[strike]]; the [[striker]]",
                         senseIter.next().getGloss().getText())
        self.assertEqual(
            "{{cricket}} Any player selected for his or her [[team]] principally to [[bat]], as opposed to a [[bowler]]",
            senseIter.next().getGloss().getText())
        self.assertFalse(senseIter.hasNext())

    def testGenderPortugueseNounMasculine(self):  # throws Exception
        page = self.parse("escritorio.txt")
        self.assertEqual(GrammaticalGender.MASCULINE, page.getEntry(0).getGender())

    def testGenderGermanNeuter(self):  # throws Exception
        page = self.parse("boot.txt")
        self.assertEqual(GrammaticalGender.NEUTER, page.getEntry(0).getGender())

    def testGenderSpanishFeminine(self):  # throws Exception
        page = self.parse("bamba.txt")
        self.assertEqual(GrammaticalGender.FEMININE, page.getEntry(0).getGender())

    def testGetRawHeadwordLine(self):  # throws Exception
        self.assertEqual("{{pt-noun|m|s}}", self.parse("escritorio.txt").getEntry(0).getRawHeadwordLine())
        self.assertEqual("{{de-noun|n|Boots|gen2=Bootes|Boote|Bötchen}}",
                         self.parse("boot.txt").getEntry(0).getRawHeadwordLine())
        self.assertEqual("{{es-noun|f}}", self.parse("bamba.txt").getEntry(0).getRawHeadwordLine())

    def testGetExamples(self):  # throws Exception
        page = self.parse("cheio.txt")
        entry = page.getEntry(0)

        examples = entry.getExamples()
        self.assertEqual(4, len(examples))

        senseFull = entry.getSense(1)
        senseCovered = entry.getSense(2)
        senseFedUp = entry.getSense(3)

        self.assertEqual(2, len(senseFull.getExamples()))
        self.assertEqual(1, len(senseCovered.getExamples()))
        self.assertEqual(1, len(senseFedUp.getExamples()))

        self.assertEqual("{{usex|lang=pt|A rua está '''cheia''' de trânsito|The street is full of traffic.}}",
                         senseFull.getExamples()[0].getText())
        self.assertEqual("{{usex|lang=pt|Estou '''cheio'''.|I'm full (not hungry anymore).}}",
                         senseFull.getExamples()[1].getText())

        self.assertEqual("A rua está '''cheia''' de óleo.", senseCovered.getExamples()[0].getText())
        self.assertEqual("The street is covered with oil.",
                         senseCovered.getExamples()[0].getTranslation().getText())
        self.assertEqual("{{usex|lang=pt|Estou '''cheio''' dele.|I'm fed up with him.}}",
                         senseFedUp.getExamples()[0].getText())

    def testGetExamplesForSubSense(self):  # throws Exception
        page = self.parse("head.txt")
        # The [[principal]] [[operative]] part of a machine.
        senseWithSubSenses = page.getEntry(0).getSense(7)
        examples = senseWithSubSenses.getExamples()
        self.assertEqual(2, len(examples))
        self.assertEqual("''Hit the nail on the '''head'''!''", examples[0].getText())
        self.assertEqual("''The '''head''' of the compass needle is pointing due north.''", examples[1].getText())

    def testGetCategories(self):  # throws Exception
        page = self.parse("head.txt")
        categories = page.getCategories()
        self.assertEqual(["1000 English basic words", "Anatomy"], categories)

    def testParseSenseSynonyms(self):  # throws Exception
        handler = ENSenseHandler()
        page = WiktionaryPage()
        context = ParsingContext(page)
        handler.processHead("", context)
        handler.processBody("# gloss", context)
        handler.processBody("#: {{syn|en|foo|bar}}", context)
        handler.processBody("#: {{synonyms|en|baz|[[quux]]}}", context)
        handler.fillContent(context)
        self.assertEqual(1, page.getEntryCount())
        self.assertEqual(1, page.getEntry(0).getSenseCount())
        synonyms = page.getEntry(0).getSense(1).getRelations(RelationType.SYNONYM)
        self.assertEqual(['foo', 'bar', 'baz', 'quux'], [synonym.getTarget() for synonym in synonyms])

    def testParseSenseAntonyms(self):  # throws Exception
        handler = ENSenseHandler()
        page = WiktionaryPage()
        context = ParsingContext(page)
        handler.processHead("", context)
        handler.processBody("# gloss", context)
        handler.processBody("#: {{ant|en|foo|bar}}", context)
        handler.processBody("#: {{antonyms|en|baz}}", context)
        handler.fillContent(context)
        self.assertEqual(1, page.getEntryCount())
        self.assertEqual(1, page.getEntry(0).getSenseCount())
        antonyms = page.getEntry(0).getSense(1).getRelations(RelationType.ANTONYM)
        self.assertEqual(["foo", "bar", "baz"], [antonym.getTarget() for antonym in antonyms])

    def testParseSynonymsAndAntonymsCombined(self):  # throws Exception
        page = self.parse("garçon.txt")
        entry = page.getEntry(0)

        self.assertEqual(3, entry.getSenseCount())
        examples = entry.getExamples()
        self.assertEqual(2, len(examples))
        self.assertEqual("{{ux|fr|Il a deux '''garçons''' et une fille.|He has two '''boys''' and a daughter.}}",
                         examples[0].getText())
        self.assertEqual("{{ux|fr|'''Garçon''', l'addition s'il vous plaît.|'''Waiter''', the bill please.|inline=1}}",
                         examples[1].getText())

        sense1 = entry.getSense(1)
        sense2 = entry.getSense(2)
        sense3 = entry.getSense(3)

        def synonyms(sense):
            return {relation.getTarget() for relation in sense.getRelations(RelationType.SYNONYM)}

        def antonyms(sense):
            return {relation.getTarget() for relation in sense.getRelations(RelationType.ANTONYM)}

        # boy
        self.assertEqual({"gamin", "fils"}, synonyms(sense1))
        self.assertEqual({"adulte"}, antonyms(sense1))
        # man
        self.assertEqual({"homme"}, synonyms(sense2))
        self.assertTrue(not antonyms(sense2))
        # waiter
        self.assertEqual({"serveur", "serviteur"}, synonyms(sense3))
        self.assertTrue(not antonyms(sense3))
