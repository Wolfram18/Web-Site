from AntiSite.wsgi import *
import math
from unittest import TestCase
from controllers.lsa import build_terms, make_tf, _count_docs_with_word, make_idf, cosine_similarity


class TestLSA(TestCase):
    def test_build_terms(self):
        documents = [["внесение изменение статья библиотечный дело организация",
                      "внесение изменение статья судебный производство",
                      "внесение изменение производство организация"],
                     ["внесение изменение статья библиотечный дело организация"],
                     []]
        expected = [{'внесение': 0, 'изменение': 1, 'статья': 2, 'библиотечный': 3,
                     'дело': 4, 'организация': 5, 'судебный': 6, 'производство': 7},
                    {'внесение': 0, 'изменение': 1, 'статья': 2, 'библиотечный': 3,
                     'дело': 4, 'организация': 5},
                    {}]
        for i in range(len(documents)):
            result = build_terms(documents[i], False)
            self.assertDictEqual(result, expected[i])

    def test_make_tf(self):
        test_terms = {'внесение': 0, 'изменение': 1, 'статья': 2,
                      'библиотечный': 3, 'дело': 4, 'организация': 5}
        documents = ["внесение изменение производство организация",
                     "внесение изменение организация организация"
                     " внесение производство производство дело",
                     ""]
        expected = [[1 / 4, 1 / 4, 0, 0, 0, 1 / 4],
                    [2 / 8, 1 / 8, 0, 0, 1 / 8, 2 / 8],
                    [0, 0, 0, 0, 0, 0]]
        for i in range(len(documents)):
            result = make_tf(documents[i], test_terms)
            self.assertEqual(result, expected[i])

    def test_count_docs_with_word(self):
        docs = ["внесение изменение статья библиотечный дело организация",
                "внесение изменение статья судебный производство",
                "внесение изменение производство организация",
                "изменение статья библиотечный дело организация",
                "внесение изменение судебный производство"]
        result = _count_docs_with_word("статья", docs)
        self.assertEqual(result, 3)

    def test_make_idf(self):
        test_terms = {'внесение': 0, 'изменение': 1, 'статья': 2,
                      'библиотечный': 3, 'дело': 4, 'организация': 5}
        documents = [["внесение изменение статья библиотечный дело организация",
                      "внесение изменение статья судебный производство",
                      "внесение изменение производство организация",
                      "изменение статья библиотечный дело организация",
                      "внесение изменение судебный производство"], [""]]
        expected = [[1 + math.log10(5 / 4), 1 + math.log10(5 / 5), 1 + math.log10(5 / 3),
                     1 + math.log10(5 / 2), 1 + math.log10(5 / 2), 1 + math.log10(5 / 3)],
                    [1, 1, 1, 1, 1, 1]]
        for i in range(len(documents)):
            result = make_idf(documents[i], test_terms)
            self.assertEqual(result, expected[i])

    def test_cosine_similarity(self):
        vec1 = [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
        vec2 = [[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        expected = [1, 0, 0]
        for i in range(len(vec1)):
            result = round(cosine_similarity(vec1[i], vec2[i]), 2)
            self.assertEqual(result, expected[i])


class TestIntegrativeLSA(TestCase):
    def test_make_tf_with_terms(self):
        documents = ["внесение изменение статья библиотечный дело организация",
                     "внесение изменение статья судебный производство",
                     "внесение изменение производство организация"]
        terms = build_terms(documents, False)
        document = "внесение изменение производство организация изменение"
        result = make_tf(document, terms)
        expected = [1 / 5, 2 / 5, 0, 0, 0, 1 / 5, 0, 1 / 5]
        self.assertEqual(result, expected)

    def test_make_idf_with_terms(self):
        documents = ["внесение изменение статья библиотечный дело организация"]
        terms = build_terms(documents, False)
        result = make_idf(documents, terms)
        expected = [1, 1, 1, 1, 1, 1]
        self.assertEqual(result, expected)
