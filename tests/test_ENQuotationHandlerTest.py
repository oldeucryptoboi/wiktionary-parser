import unittest

from tests import *
from compat import *


class ENQuotationHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):
    """ Test case for {@link ENQuotationHandler}. """

    def testBe(self):  # throws Exception
        page = self.parse("be.txt")
        sense = page.getEntry(0).getSense(3)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        self.assertEqual("'''1526''', ''Bible'', tr. William Tyndale, Matthew 2:", quotation.getSource().getText())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual("Rachel wepynge ffor her chyldren, and wolde nott be comforted because they '''were''' not.",
                         quotation.getLines()[0].getText())
        quotation = quotationIter.next()
        self.assertEqual("'''c. 1600''', [[w:William Shakespeare|William Shakespeare]], ''[[s:Hamlet|Hamlet]]'':",
                         quotation.getSource().getText())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual("''To '''be''' or not to '''be''', that is the question.''",
                         quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())

        sense = page.getEntry(0).getSense(10)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        # self.assertEqual("{{quote-book|year=1995|author=C. K. Ogden|title=Psyche: An Annual General and Linguistic Psychology 1920-1952|pageurl=http://books.google.com.br/books?id=43QCzKUXkBYC&amp;pg=PA13#v=onepage&amp;q&amp;f=false|isbn=9780415127790|page=13|publisher=C. K. Ogden|passage=Study courses of Esperanto and Ido have '''been''' broadcast.}}", quotation.getSource().getText())
        self.assertIsNone(quotation.getSource())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual(
            "{{quote-book|year=1995|author=C. K. Ogden|title=Psyche: An Annual General and Linguistic Psychology 1920-1952|pageurl=http://books.google.com.br/books?id=43QCzKUXkBYC&amp;pg=PA13#v=onepage&amp;q&amp;f=false|isbn=9780415127790|page=13|publisher=C. K. Ogden|passage=Study courses of Esperanto and Ido have '''been''' broadcast.}}",
            quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())

        sense = page.getEntry(0).getSense(11)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        # self.assertEqual("{{quote-book|year=1995|author=C. K. Ogden|title=Psyche: An Annual General and Linguistic Psychology 1920-1952|pageurl=http://books.google.com.br/books?id=43QCzKUXkBYC&amp;pg=PA13#v=onepage&amp;q&amp;f=false|isbn=9780415127790|page=13|publisher=C. K. Ogden|passage=In the possibility of radio uses of a constructed language — and such experiments '''are''' proving successful — vast sums of money and untold social forces may be involved.}}", quotation.getSource().getText())
        self.assertIsNone(quotation.getSource())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual(
            "{{quote-book|year=1995|author=C. K. Ogden|title=Psyche: An Annual General and Linguistic Psychology 1920-1952|pageurl=http://books.google.com.br/books?id=43QCzKUXkBYC&amp;pg=PA13#v=onepage&amp;q&amp;f=false|isbn=9780415127790|page=13|publisher=C. K. Ogden|passage=In the possibility of radio uses of a constructed language — and such experiments '''are''' proving successful — vast sums of money and untold social forces may be involved.}}",
            quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())

        sense = page.getEntry(0).getSense(12)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        self.assertEqual(
            "'''1850''', [[w:Dante Gabriel Rossetti|Dante Gabriel Rossetti]], ''The Blessed Damozel'', lines 67-68",
            quotation.getSource().getText())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual("‘I wish that he '''were''' come to me, / For he will come,’ she said.",
                         quotation.getLines()[0].getText())
        quotation = quotationIter.next()
        self.assertEqual("'''1922''', [[w:A. E. Housman|A. E. Housman]], [[w:Last Poems|Last Poems]] XXV, line 13",
                         quotation.getSource().getText())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual("''The King with half the East at heel '''is''' marched from lands of morning;''",
                         quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())

    def testNonsense(self):  # throws Exception
        page = self.parse("nonsense.txt")
        sense = page.getEntry(0).getSense(3)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        self.assertEqual(
            "'''2008''', &quot;Nick Leeson has some lessons for this collapse&quot;, Telegraph.co.uk, Oct 9, 2008",
            quotation.getSource().getText())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual(
            "and central banks lend vast sums against marshmallow backed securities, or other '''nonsenses''' creative bankers dreamed up.",
            quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())

    def testPlant(self):  # throws Exception {
        page = self.parse("plant.txt")
        sense = page.getEntry(1).getSense(3)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        # self.assertEqual("{{quote-news|year=2011|date=January 15|author=Sam Sheringham|title=Chelsea 2 - 0 Blackburn Rovers|work=BBC|url=http://news.bbc.co.uk/sport2/hi/football/eng_prem/9358426.stm|page=|passage=First Anelka curled a shot wide from just outside the box, then Lampard '''planted''' a header over the bar from Bosingwa's cross. }}", quotation.getSource().getText())
        self.assertIsNone(quotation.getSource())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual(
            "{{quote-news |year=2011 |date=January 15 |author=Sam Sheringham |title=Chelsea 2 - 0 Blackburn Rovers |work=BBC |url=http://news.bbc.co.uk/sport2/hi/football/eng_prem/9358426.stm |page= |passage=First Anelka curled a shot wide from just outside the box, then Lampard '''planted''' a header over the bar from Bosingwa's cross. }}",
            quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())

        sense = page.getEntry(1).getSense(4)
        quotationIter = List(sense.getQuotations()).iterator()
        quotation = quotationIter.next()
        self.assertEqual("'''2007''', Richard Laymon, ''Savage'', page 118:", quotation.getSource().getText())
        self.assertEqual(1, len(quotation.getLines()))
        self.assertEqual(
            "Sarah, she kissed each of her grandparents on the forehead. They were '''planted''' in a graveyard behind the church.",
            quotation.getLines()[0].getText())
        self.assertFalse(quotationIter.hasNext())
