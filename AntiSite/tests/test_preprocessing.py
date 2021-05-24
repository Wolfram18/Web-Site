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


class TestCutBeginning(TestCase):
    def test_after_resolution(self):
        source = "1 ПОСТАНОВЛЕНИЕ 2 ФЕДЕРАЛЬНЫЙ ЗАКОН 3"
        result = cut_beginning(source)
        self.assertEqual(result, " 2 ФЕДЕРАЛЬНЫЙ ЗАКОН 3")

    def test_after_federal(self):
        source = "1 ФЕДЕРАЛЬНЫЙ ЗАКОН 2 ПОСТАНОВЛЕНИЕ 3"
        result = cut_beginning(source)
        self.assertEqual(result, " 2 ПОСТАНОВЛЕНИЕ 3")

    def test_after_resolution_with_spaces(self):
        source = "1 П О С Т А Н О В Л Е Н И Е 2 Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н 3"
        result = cut_beginning(source)
        self.assertEqual(result, " 2 Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н 3")

    def test_after_federal_with_spaces(self):
        source = "1 Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н 2 П О С Т А Н О В Л Е Н И Е 3"
        result = cut_beginning(source)
        self.assertEqual(result, " 2 П О С Т А Н О В Л Е Н И Е 3")

    def test_only_resolution(self):
        source = "1 ПОСТАНОВЛЕНИЕ 2"
        result = cut_beginning(source)
        self.assertEqual(result, " 2")

    def test_only_federal(self):
        source = "1 ФЕДЕРАЛЬНЫЙ ЗАКОН 2"
        result = cut_beginning(source)
        self.assertEqual(result, " 2")

    def test_all_law(self):
        source = "123"
        result = cut_beginning(source)
        self.assertEqual(result, "123")


class TestCutEnd(TestCase):
    def test_before_scroll(self):
        source = "1 ПЕРЕЧЕНЬ 2 ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ 3"
        result = cut_end(source)
        self.assertEqual(result, "1 ")

    def test_before_scroll_with_spaces(self):
        source = "1 П Е Р Е Ч Е Н Ь 2 ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ 3"
        result = cut_end(source)
        self.assertEqual(result, "1 ")

    def test_before_finance(self):
        source = "1 ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ 2 ПЕРЕЧЕНЬ 3"
        result = cut_end(source)
        self.assertEqual(result, "1 ")

    def test_all_text(self):
        source = "123"
        result = cut_end(source)
        self.assertEqual(result, "123")


class TestIOError(TestCase):
    def test_generate_stopwords(self):
        with self.assertRaises(IOError, msg="File 'stopwords' does not exist!"):
            generate_stopwords('stopwords.txt')

    def test_delete_irrelevant_words(self):
        with self.assertRaises(IOError, msg="File 'irrelevant_words' does not exist!"):
            delete_irrelevant_words("source", "irrelevant_words.txt")


class TestCanonize(TestCase):
    def test_law1(self):
        russian_stopwords = generate_stopwords_for_test()
        source = "О внесении изменения в статью 7 Федерального закона «О ветеранах»"
        result = canonize(source, russian_stopwords)
        self.assertEqual(result, ['внесение', 'изменение', 'статья', 'федеральный', 'закон', 'ветеран'])

    def test_law2(self):
        russian_stopwords = generate_stopwords_for_test()
        source = "О внесении изменений в Трудовой кодекс Российской Федерации"
        result = canonize(source, russian_stopwords)
        self.assertEqual(result, ['внесение', 'изменение', 'трудовой', 'кодекс', 'российский', 'федерация'])

    def test_law3(self):
        russian_stopwords = generate_stopwords_for_test()
        source = "О внесении изменений в Федеральный закон 'О социальной помощи'"
        result = canonize(source, russian_stopwords)
        self.assertEqual(result, ['внесение', 'изменение', 'федеральный', 'закон', 'социальный', 'помощь'])

    def test_law4(self):
        russian_stopwords = generate_stopwords_for_test()
        source = "О внесении изменений в Уголовный кодекс Российской Федерации"
        result = canonize(source, russian_stopwords)
        self.assertEqual(result, ['внесение', 'изменение', 'уголовный', 'кодекс', 'российский', 'федерация'])

    def test_law5(self):
        russian_stopwords = generate_stopwords_for_test()
        source = "О внесении изменений в Федеральный закон „О детях войны„"
        result = canonize(source, russian_stopwords)
        self.assertEqual(result, ['внесение', 'изменение', 'федеральный', 'закон', 'ребёнок', 'война'])


class TestCanonizeWord(TestCase):
    def test_lower(self):
        source = "ФеДеРаЛьНыЙ"
        result = canonize_word(source)
        self.assertEqual(result, "федеральный")

    def test_delete_spec(self):
        source = "«фе8де5ральный?»"
        result = canonize_word(source)
        self.assertEqual(result, "федеральный")

    def test_normal_form(self):
        source = "федерального"
        result = canonize_word(source)
        self.assertEqual(result, "федеральный")

    def test_all(self):
        source = "Федерального!!!"
        result = canonize_word(source)
        self.assertEqual(result, "федеральный")


class TestDeleteTag(TestCase):
    def test_delete_tag_right(self):
        source = "</Федеральный</>"
        result = delete_tag(source)
        self.assertEqual(result, "Федеральный")

    def test_delete_tag_left(self):
        source = "</>Федеральный/>"
        result = delete_tag(source)
        self.assertEqual(result, "Федеральный")

    def test_delete_wrong_tag(self):
        source = "</Федеральный/>"
        result = delete_tag(source)
        self.assertEqual(result, "Федеральный")
