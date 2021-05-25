import math

from AntiSite.wsgi import *
from unittest import TestCase
from controllers.lsa import build_terms, make_tf, _count_docs_with_word, make_idf, cosine_similarity


class TestBuildTerms(TestCase):
    def test_for_many_docs(self):
        documents = ["внесение изменение статья библиотечный дело организация",
                     "внесение изменение статья судебный производство",
                     "внесение изменение производство организация"]
        result = build_terms(documents)
        expected = {'внесение': 0, 'изменение': 1, 'статья': 2, 'библиотечный': 3,
                    'дело': 4, 'организация': 5, 'судебный': 6, 'производство': 7}
        self.assertDictEqual(result, expected)

    def test_for_one_doc(self):
        documents = ["внесение изменение статья библиотечный дело организация"]
        result = build_terms(documents)
        expected = {'внесение': 0, 'изменение': 1, 'статья': 2, 'библиотечный': 3, 'дело': 4, 'организация': 5}
        self.assertDictEqual(result, expected)

    def test_for_zero_docs(self):
        documents = []
        result = build_terms(documents)
        expected = {}
        self.assertDictEqual(result, expected)


class TestMakeTF(TestCase):
    test_terms = {'внесение': 0, 'изменение': 1, 'статья': 2, 'библиотечный': 3, 'дело': 4, 'организация': 5}

    def test_once(self):
        document = "внесение изменение производство организация"
        result = make_tf(document, self.test_terms)
        expected = [1 / 4, 1 / 4, 0, 0, 0, 1 / 4]
        self.assertEqual(result, expected)

    def test_many(self):
        document = "внесение изменение организация организация внесение производство производство дело"
        result = make_tf(document, self.test_terms)
        expected = [2 / 8, 1 / 8, 0, 0, 1 / 8, 2 / 8]
        self.assertEqual(result, expected)

    def test_zero(self):
        document = ""
        result = make_tf(document, self.test_terms)
        expected = [0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)

    # совместный
    def test_with_terms(self):
        documents = ["внесение изменение статья библиотечный дело организация",
                     "внесение изменение статья судебный производство",
                     "внесение изменение производство организация"]
        terms = build_terms(documents)
        document = "внесение изменение производство организация изменение"
        result = make_tf(document, terms)
        expected = [1 / 5, 2 / 5, 0, 0, 0, 1 / 5, 0, 1 / 5]
        self.assertEqual(result, expected)


class TestMakeIDF(TestCase):
    test_terms = {'внесение': 0, 'изменение': 1, 'статья': 2, 'библиотечный': 3, 'дело': 4, 'организация': 5}
    docs = ["внесение изменение статья библиотечный дело организация",
            "внесение изменение статья судебный производство",
            "внесение изменение производство организация",
            "изменение статья библиотечный дело организация",
            "внесение изменение судебный производство"]

    def test_count_docs_with_word(self):
        result = _count_docs_with_word("статья", self.docs)
        self.assertEqual(result, 3)

    def test_many(self):
        result = make_idf(self.docs, self.test_terms)
        expected = [1 + math.log10(5 / 4), 1 + math.log10(5 / 5), 1 + math.log10(5 / 3),
                    1 + math.log10(5 / 2), 1 + math.log10(5 / 2), 1 + math.log10(5 / 3)]
        self.assertEqual(result, expected)

    def test_zero(self):
        documents = ""
        result = make_tf(documents, self.test_terms)
        expected = [0, 0, 0, 0, 0, 0]
        self.assertEqual(result, expected)

    # совместный
    def test_with_terms(self):
        documents = ["внесение изменение статья библиотечный дело организация"]
        terms = build_terms(documents)
        result = make_idf(documents, terms)
        expected = [1, 1, 1, 1, 1, 1]
        self.assertEqual(result, expected)


class TestCosineSimilarity(TestCase):
    def test_identical(self):
        vec1 = [1, 1, 1, 1, 1, 1]
        vec2 = [1, 1, 1, 1, 1, 1]
        result = round(cosine_similarity(vec1, vec2))
        expected = 1
        self.assertEqual(result, expected)

    def test_different(self):
        vec1 = [1, 1, 1, 1, 1, 1]
        vec2 = [0, 0, 0, 0, 0, 0]
        result = round(cosine_similarity(vec1, vec2))
        expected = 0
        self.assertEqual(result, expected)

    def test_zero(self):
        vec1 = [0, 0, 0, 0, 0, 0]
        vec2 = [0, 0, 0, 0, 0, 0]
        result = round(cosine_similarity(vec1, vec2))
        expected = 0
        self.assertEqual(result, expected)