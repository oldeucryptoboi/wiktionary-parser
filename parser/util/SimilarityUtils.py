import re
import math


class SimilarityUtils:
    """ Some convenient string utilities. """

    NGRAM_PATTERN = re.compile("^_?[^0-9\\?!\\-_/]*_?$")  

    @classmethod
    def computeNGrams(cls, startOrder, maxOrder, text):
        """ Compute N Grams.
            @param startOrder
            @param maxOrder
            @param text
            @return a n gram to frequency map. """
        ngram2count = dict()
        tokens = re.split("\\s", text)

        for order in range(startOrder, maxOrder+1):
            for token in tokens:
                token = "_" + token + "_"

                for i in range(len(token) - order + 1):
                    ngram = token[i:i + order]

                    if not cls.NGRAM_PATTERN.match(ngram):
                        continue
                    elif ngram not in ngram2count:
                        ngram2count[ngram] = 1
                    else:
                        score = ngram2count.pop(ngram)
                        score += 1
                        ngram2count[ngram] = score

        if "_" in ngram2count.keys():
            blanksScore = ngram2count.pop("_")
            ngram2count["_"] = blanksScore / 2

        return ngram2count

    @staticmethod
    def computeWord2count(text):
        """ Calculate word frequency.
            @param text a text to process
            @return a map of word to frequency. """
        word2count = dict()
        wordPattern = re.compile("\\w+")  
        for matcher in re.finditer(wordPattern, text):
            w = matcher.group().lower()
            if w in word2count.keys():
                word2count[w] = word2count[w] + 1
            else:
                word2count[w] = 1

        return word2count

    @staticmethod
    def ngramSim(ngramsA, ngramsB):
        """ Calculate similarity between two sets of n grams
            @param ngramsA a set of n grams
            @param ngramsB a set of n grams
            @return the similarity value. """
        a = 0.0
        b = 0.0
        common = 0.0
        all_ = 0.0
        ngramAll = dict(ngramsB)
        for key, value in ngramsA.items():
            if key in ngramAll:
                if ngramAll[key] < value:
                    ngramAll[key] = value
                else:
                    value = ngramAll[key]
            else:
                ngramAll[value] = value

            all_ += value

        for nGramACount in ngramsA.values():
            a += math.log(nGramACount / all_)
        for nGramBCount in ngramsB.values():
            b += math.log(nGramBCount / all_)

        for key, value in ngramsA.items():
            if key in ngramsB:
                count = ngramAll[key]
                if count < value:
                    common += math.log(count / all_)
                else:
                    common += math.log(value / all_)
        try:
            return 2 * common / (a + b)
        except ZeroDivisionError:
            return float('nan')

    @classmethod
    def textSim(cls, textA, textB):
        """ Calculate similarity between two text based on trigram.
            @param textA text A
            @param textB text B
            @return similarity value """
        ngramA = cls.computeNGrams(3, 3, textA)
        ngramB = cls.computeNGrams(3, 3, textB)

        return cls.ngramSim(ngramA, ngramB)

    @classmethod
    def wordSim(cls, textA, textB):
        """ Calculate string similarity based on ugram of words.
            @param textA text A
            @param textB text B
            @return similarity value """
        ngramA = cls.computeWord2count(textA)
        ngramB = cls.computeWord2count(textB)

        return cls.ngramSim(ngramA, ngramB)

    @classmethod
    def triSim(cls, textA, textB):
        """ Trigram similarity measure
            @param textA text A
            @param textB text B
            @return trigram similarity value """
        ngramA = cls.computeNGrams(3, 3, textA)
        ngramB = cls.computeNGrams(3, 3, textB)
        common = 0
        allA = 0
        allB = 0
        for count in ngramA.values():
            allA += count

        for count in ngramB.values():
            allB += count

        for ngram in ngramA.keySet():
            if ngram in ngramB:
                countA = ngramA.get(ngram)
                countB = ngramB.get(ngram)
                if countA < countB:
                    common += countA
                else:
                    common += countB

        return 1.0 / (1.0 + allA + allB - 2 * common)
