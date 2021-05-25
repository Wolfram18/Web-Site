from AntiSite.wsgi import *
from unittest import TestCase

from controllers.lsa import compare_for_underline_canon, compare_for_underline_text


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


class TestUnderlineCanon(TestCase):
    def test_true_compare(self):
        canon_main_array = ["внесение", "изменение", "судебный", "производство"]
        canon_cmp_array = ["внесение", "изменение", "статья", "библиотечный", "производство", "организация"]
        result = compare_for_underline_canon(canon_main_array, canon_cmp_array)
        expected = ("<mark>внесение</mark> <mark>изменение</mark> "
                    "судебный <mark>производство</mark> ",
                    "<mark>внесение</mark> <mark>изменение</mark> статья "
                    "библиотечный <mark>производство</mark> организация ")
        self.assertEqual(result, expected)

    def test_empty_main_array(self):
        canon_main_array = []
        canon_cmp_array = ["внесение", "изменение", "статья", "библиотечный", "производство", "организация"]
        result = compare_for_underline_canon(canon_main_array, canon_cmp_array)
        expected = ("", "внесение изменение статья библиотечный производство организация ")
        self.assertEqual(result, expected)

    def test_empty_cmp_array(self):
        canon_main_array = ["внесение", "изменение", "статья", "библиотечный", "производство", "организация"]
        canon_cmp_array = []
        result = compare_for_underline_canon(canon_main_array, canon_cmp_array)
        expected = ("внесение изменение статья библиотечный производство организация ", "")
        self.assertEqual(result, expected)


class TestUnderlineText(TestCase):
    def test_true_compare(self):
        canon_main_array = ['внесение', 'изменение', 'статья', 'федеральный', 'закон', 'ветеран']
        main_text_array = ['О', 'внесении', 'изменения', 'в', 'статью', '7',
                           'Федерального', 'закона', '«О', 'ветеранах»']
        canon_cmp_array = ['внесение', 'изменение', 'трудовой', 'кодекс', 'российский', 'федерация']
        text_cmp = "О внесении изменений в Трудовой кодекс Российской Федерации"
        russian_stopwords = generate_stopwords_for_test()
        result = compare_for_underline_text(canon_main_array, main_text_array,
                                            canon_cmp_array, text_cmp, russian_stopwords)
        expected = ("О <mark>внесении</mark> <mark>изменения</mark> в статью 7 Федерального закона «О ветеранах» ",
                    "О <mark>внесении</mark> <mark>изменений</mark> в Трудовой кодекс Российской Федерации ")
        self.assertEqual(result, expected)

    def test_empty_main(self):
        canon_main_array = []
        main_text_array = []
        canon_cmp_array = ['внесение', 'изменение', 'трудовой', 'кодекс', 'российский', 'федерация']
        text_cmp = "О внесении изменений в Трудовой кодекс Российской Федерации"
        russian_stopwords = generate_stopwords_for_test()
        result = compare_for_underline_text(canon_main_array, main_text_array,
                                            canon_cmp_array, text_cmp, russian_stopwords)
        expected = ("", "О внесении изменений в Трудовой кодекс Российской Федерации ")
        self.assertEqual(result, expected)

    def test_empty_cmp(self):
        canon_main_array = ['внесение', 'изменение', 'статья', 'федеральный', 'закон', 'ветеран']
        main_text_array = ['О', 'внесении', 'изменения', 'в', 'статью', '7',
                           'Федерального', 'закона', '«О', 'ветеранах»']
        canon_cmp_array = []
        text_cmp = ""
        russian_stopwords = generate_stopwords_for_test()
        result = compare_for_underline_text(canon_main_array, main_text_array,
                                            canon_cmp_array, text_cmp, russian_stopwords)
        expected = ("О внесении изменения в статью 7 Федерального закона «О ветеранах» ", "")
        self.assertEqual(result, expected)