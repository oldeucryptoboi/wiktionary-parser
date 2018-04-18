class WordFormHandlerTest:

    handler = None

    def assertFalse(self):
        pass

    def assertTrue(self):
        pass

    # https://en.wiktionary.org/wiki/Template:wikipedia
    def testIgnoreWikipedia(self):
        self.assertFalse(self.handler.parse("{{wikipedia}}"))
        self.assertFalse(self.handler.parse("{{wikipedia|lang=de}}"))
        self.assertFalse(self.handler.parse("{{Wikipedia}}"))

    # redirects Template:wikipedia
    def testIgnoreWiki(self):
        self.assertFalse(self.handler.parse("{{wiki}}"))
        self.assertFalse(self.handler.parse("{{Wiki}}"))

    # https://en.wiktionary.org/wiki/Template:slim-wikipedia
    def testIgnoreSlimWikipedia(self):
        self.assertFalse(self.handler.parse("{{slim-wikipedia}}"))
        self.assertFalse(self.handler.parse("{{slim-wikipedia|lang=de}}"))

    # https://en.wiktionary.org/wiki/Template:wikiquote
    def testIgnoreWikiquote(self):
        self.assertFalse(self.handler.parse("{{wikiquote}}"))

    # https://en.wiktionary.org/wiki/Template:wikiversity
    def testIgnoreWikiversity(self):
        self.assertFalse(self.handler.parse("{{wikiversity}}"))

    # https://en.wiktionary.org/wiki/Template:wikispecies
    def testIgnoreWikispecies(self):
        self.assertFalse(self.handler.parse("{{wikispecies}}"))
        self.assertFalse(self.handler.parse("{{wikispecies|Popillia japonica}}"))

    # https://en.wiktionary.org/wiki/Template:examples
    # https://en.wiktionary.org/wiki/Template:examples-right
    def testIgnoreExamples(self):
        self.assertFalse(self.handler.parse("{{examples|Foo}}"))
        self.assertFalse(self.handler.parse("{{examples-right|Foo}}"))

    # https://en.wiktionary.org/wiki/Template:enum
    def testIgnoreEnum(self):
        self.assertFalse(self.handler.parse("{{enum|Foo}}"))

    # https://en.wiktionary.org/wiki/Template:no_entry
    def testIgnoreNoEntry(self):
        self.assertFalse(self.handler.parse("{{no entry|}}"))

    def testIgnoreImageLinks(self):
        self.assertFalse(self.handler.parse("[[File:Foo.jpg|thumb|right|Bar]]"))

    # https://en.wiktionary.org/wiki/Template:rfc-header
    def testIgnoreRfcHeader(self):
        self.assertFalse(self.handler.parse("{{rfc-header|Abbreviation}}"))

    # https://en.wiktionary.org/wiki/Template:rfc
    def testIgnoreRfc(self):
        self.assertFalse(self.handler.parse("{{rfc|a reason}}"))

    # https://en.wiktionary.org/wiki/Template:attention
    def testIgnoreAttentionHeader(self):
        self.assertFalse(self.handler.parse("{{attention|de|needs a headword}}"))

    def testGetRawHeadwordLineLegacyPattern(self):  # throws Exception
        self.assertTrue(self.handler.parse("'''Atheismus''' {{g|m}}"))
        self.assertEqual("'''Atheismus''' {{g|m}}", self.handler.getRawHeadwordLine())

    def testGetRawHeadwordLineTemplatePattern(self):  # throws Exception
        self.assertTrue(self.handler.parse("{{some-template}}"))
        self.assertEqual("{{some-template}}", self.handler.getRawHeadwordLine())

    def testGetRawHeadwordLineTemplatePatternOnlyParseOnce(self):  # throws Exception
        self.assertTrue(self.handler.parse("{{some-template}}"))
        self.assertFalse(self.handler.parse("{{some-other-template}}"))
        self.assertEqual("{{some-template}}", self.handler.getRawHeadwordLine())
