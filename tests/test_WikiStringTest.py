import unittest
from api.entry import WikiString


class TestWikiString(unittest.TestCase):

    def testplainText(self):
        text = "* {{sense|of or pertaining to the abdomen}} [[ventral]]"
        w = WikiString(text)
        self.assertEqual("ventral", w.getPlainText())

        text = "# {{zoology|obsolete}} Belonging to the [[abdominales|Abdominales]]; as, ''abdominal'' fishes."
        w = WikiString(text)
        self.assertEqual("# Belonging to the Abdominales; as, abdominal fishes.", w.getPlainText())

        text = ":[1] [[eukaryotisch]]es [[Lebewesen|Lebw.]], das keine [[Photosynthese]] betreiben kann, [[Sauerstoff]] zur [[Atmung]] benötigt und tierischen und/oder pflanzlichen Organismen als [[Nahrung]] zu sich nimmt"
        w = WikiString(text)
        self.assertEqual(
            "[1] eukaryotisches Lebw., das keine Photosynthese betreiben kann, Sauerstoff zur Atmung benötigt und tierischen und/oder pflanzlichen Organismen als Nahrung zu sich nimmt",
            w.getPlainText())

        text = ":[1] \"Die ''Welt'' ist schon oft mit einem Narrenhause verglichen worden.\"<ref>[http://www.humanist.de/religion/pfaffe.html Otto von Corvin, Der Pfaffenspiegel] </ref>"
        w = WikiString(text)
        self.assertEqual("[1] \"Die Welt ist schon oft mit einem Narrenhause verglichen worden.\"", w.getPlainText())

        text = ":[1–10] {{Wikipedia|Welt (Begriffsklärung)}}"
        w = WikiString(text)
        self.assertEqual("[1–10]", w.getPlainText())

    def testremoveWikiLinks(self):  # throws Exception
        self.assertEqual("Leader", WikiString.removeWikiLinks("[[leader|Leader]]"))
        self.assertEqual("Leader", WikiString.removeWikiLinks("[[Leader]]"))


if __name__ == '__main__':
    unittest.main()
