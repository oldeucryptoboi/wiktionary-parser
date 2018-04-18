import unittest

from api.util import TemplateParser


class TestTemplateParser(unittest.TestCase):

    def testTemplateParser(self):
        text = "From {{etyl|fr}}..."
        self.assertEqual(text, TemplateParser.parse(text, None))

        text = "From {{etyl|fr}}...{{etyl|de}}.. End."
        self.assertEqual(text, TemplateParser.parse(text, None))

        text = "From {{etyl|enm}} {{term|dogge|lang=enm}}, from {{etyl|ang}} {{term|docga|lang=ang||hound, powerful breed of dog}}, a pet-form diminutive of {{etyl|ang|-}} {{recons|docce|docce|lang=ang|muscle}} (found in compound {{term|fingerdocce||lang=ang|finger-muscle}} with suffix {{term|-ga|-ga|lang=ang}} (compare {{term|frocga||lang=ang|frog}}, {{term|picga||lang=ang|pig}}), from {{etyl|gem-pro|en}} {{recons|dukkōn||power, strength, muscle|lang=gem-pro}}. More at [[dock]]. In the 16th century, it superseded {{etyl|ang|-}} {{term|hund|lang=ang}} and was adopted by many continental European languages.<ref>{{R:Online Etymology Dictionary|dog}}</ref>"

        # self.assertEqual("From Middle English dogge, from Old English docga (“hound, powerful breed of dog”), a pet-form diminutive of Old English *docce (“muscle”) (found in compound fingerdocce (“finger-muscle”) with suffix -ga (compare frocga (“frog”), picga (“pig”)), from Proto-Germanic *dukkōn (“power, strength, muscle”). More at [[dock]]. In the 16th century, it superseded Old English hund and was adopted by many continental European languages.<ref></ref>",

        expected = "From Middle English dogge, from Old English docga (“hound, powerful breed of dog”), a pet-form diminutive of Old English *docce (“muscle”) (found in compound fingerdocce (“finger-muscle”) with suffix -ga (compare frocga (“frog”), picga (“pig”)), from {gem-pro} *dukkōn (“power, strength, muscle”). More at [[dock]]. In the 16th century, it superseded Old English hund and was adopted by many continental European languages.<ref></ref>"
        self.assertEqual(expected, TemplateParser.parse(text, TemplateParser.EtymologyTemplateHandler()))
