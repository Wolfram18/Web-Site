from AntiSite.wsgi import *
from unittest import TestCase
from supporting.preprocessing import generate_stopwords, canonize, cut_end, cut_beginning, canonize_word, \
    delete_irrelevant_words, delete_tag


def generate_stopwords_for_test():
    from nltk.corpus import stopwords
    russian_stopwords = stopwords.words("russian")
    line = "а б без более больше быть будто бы в вы вдруг ведь во вот впрочем все весь всегда всего г где говорить д " \
           "да даже два для до другой е если есть ещё еще ё ж же з за зачем здесь и из или иногда й к как кажется " \
           "какой когда конечно который кто куда л ли м между много может можно мой мы н ни нибудь никогда ничего но " \
           "ну не нет на над надо наконец нельзя о он она они об один опять от п при про по под перед после потом " \
           "потому почти р раз разве с сам свое своё себя сегодня сейчас сказать со совсем т ты так там тем такой " \
           "теперь то тогда тоже только том тот тут три у уж уже ф х хорошо хоть ц ч что через чтоб чтобы чуть ш щ ъ " \
           "ы ь э этот ю я ст n i fa "
    words = line.split()
    russian_stopwords.extend(words)
    return russian_stopwords


class TestPreprocessing(TestCase):
    def test_cut_beginning(self):
        source = ["1 ПОСТАНОВЛЕНИЕ 2 ФЕДЕРАЛЬНЫЙ ЗАКОН 3",
                  "1 ФЕДЕРАЛЬНЫЙ ЗАКОН 2 ПОСТАНОВЛЕНИЕ 3",
                  "1 П О С Т А Н О В Л Е Н И Е 2 Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н 3",
                  "1 Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н 2 П О С Т А Н О В Л Е Н И Е 3",
                  "1 ПОСТАНОВЛЕНИЕ 2",
                  "1 ФЕДЕРАЛЬНЫЙ ЗАКОН 2",
                  "123"]
        expected = [" 2 ФЕДЕРАЛЬНЫЙ ЗАКОН 3",
                    " 2 ПОСТАНОВЛЕНИЕ 3",
                    " 2 Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н 3",
                    " 2 П О С Т А Н О В Л Е Н И Е 3",
                    " 2",
                    " 2",
                    "123"]
        for i in range(len(source)):
            result = cut_beginning(source[i])
            self.assertEqual(result, expected[i])

    def test_cut_end(self):
        source = ["1 ПЕРЕЧЕНЬ 2 ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ 3",
                  "1 П Е Р Е Ч Е Н Ь 2 ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ 3",
                  "1 ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ 2 ПЕРЕЧЕНЬ 3",
                  "123"]
        expected = ["1 ", "1 ", "1 ", "123"]
        for i in range(len(source)):
            result = cut_end(source[i])
            self.assertEqual(result, expected[i])

    def test_canonize(self):
        russian_stopwords = generate_stopwords_for_test()
        source = ["О внесении изменения в статью 7 Федерального закона «О ветеранах»",
                  "О внесении изменений в Трудовой кодекс Российской Федерации",
                  "О внесении изменений в Федеральный закон 'О социальной помощи'",
                  "О внесении изменений в Уголовный кодекс Российской Федерации",
                  "О внесении изменений в Федеральный закон „О детях войны„"]
        expected = [['внесение', 'изменение', 'статья', 'федеральный', 'закон', 'ветеран'],
                    ['внесение', 'изменение', 'трудовой', 'кодекс', 'российский', 'федерация'],
                    ['внесение', 'изменение', 'федеральный', 'закон', 'социальный', 'помощь'],
                    ['внесение', 'изменение', 'уголовный', 'кодекс', 'российский', 'федерация'],
                    ['внесение', 'изменение', 'федеральный', 'закон', 'ребёнок', 'война']]
        for i in range(len(source)):
            result = canonize(source[i], russian_stopwords)
            self.assertEqual(result, expected[i])

    def test_canonize_word(self):
        source = ["ФеДеРаЛьНыЙ", "«фе8де5ральный?»", "федерального", "Федерального!!!",
                  "1111федеральный1111", "фе:д6%ера!льн:ый", "федера№2!льный", "()федер-+альный()"]
        expected = "федеральный"
        for i in range(len(source)):
            result = canonize_word(source[i])
            self.assertEqual(result, expected)

    def test_delete_tag(self):
        source = ["</Федеральный</>", "</>Федеральный/>", "</Федеральный/>",
                  "</</>Федеральный/>", "</Федерал</>ьный/>", "</Федеральный</>/>"]
        expected = "Федеральный"
        for i in range(len(source)):
            result = delete_tag(source[i])
            self.assertEqual(result, expected)


class TestIOError(TestCase):
    def test_generate_stopwords(self):
        with self.assertRaises(IOError, msg="File 'stopwords' does not exist!"):
            generate_stopwords('stopwords.txt')

    def test_delete_irrelevant_words(self):
        with self.assertRaises(IOError, msg="File 'irrelevant_words' does not exist!"):
            delete_irrelevant_words("source", "irrelevant_words.txt")
