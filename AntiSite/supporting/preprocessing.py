# nltk.download()
import string
import pymorphy2


# вырезать до ПОСТАНОВЛЕНИЕ и ФЕДЕРАЛЬНЫЙ ЗАКОН
def cut_beginning(source):
    def find_index(heading, heading_with_spaces):
        find_index_head = source.find(heading)
        find_index_head_spaces = source.find(heading_with_spaces)
        if find_index_head != -1:
            index = find_index_head + len(heading)
        elif find_index_head_spaces != -1:
            index = find_index_head_spaces + len(heading_with_spaces)
        else:
            index = 0
        return index

    index_res = find_index("ПОСТАНОВЛЕНИЕ", "П О С Т А Н О В Л Е Н И Е")
    index_fed = find_index("ФЕДЕРАЛЬНЫЙ ЗАКОН", "Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н")

    if index_res == 0:
        return source[index_fed:]
    elif index_fed == 0:
        return source[index_res:]
    if index_res > index_fed:
        return source[index_fed:]
    elif index_res < index_fed:
        return source[index_res:]
    else:
        return source


# вырезать после ПЕРЕЧЕНЬ и ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ
def cut_end(source):
    if source.find("ПЕРЕЧЕНЬ") != -1:
        source = source[:source.find("ПЕРЕЧЕНЬ")]
    elif source.find("П Е Р Е Ч Е Н Ь") != -1:
        source = source[:source.find("П Е Р Е Ч Е Н Ь")]

    if source.find("ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ") != -1:
        source = source[:source.find("ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ")]

    return source


def generate_stopwords(config):
    # 'supporting/stopwords.txt'
    # базовый словарь
    from nltk.corpus import stopwords
    russian_stopwords = stopwords.words("russian")

    # расширение словаря
    try:
        file = open(config, encoding='utf-8')
        line = file.read()
        words = line.split()
        russian_stopwords.extend(words)
    except IOError:
        raise IOError("File 'stopwords' does not exist!")

    return russian_stopwords


def canonize(source, russian_stopwords):
    # приведение к нижнему регистру
    source = source.lower()
    # print('Нижний регистр:', source)

    # удаление пунктуации и цифр
    spec_chars = string.punctuation + string.digits + '\n\r\t\xa0№«»—…„'
    source = "".join([ch for ch in source if ch not in spec_chars])
    # print('Без символов:', source)

    # токенизация и удаление стоп-слов
    from nltk.tokenize import word_tokenize
    source = [x for x in word_tokenize(source, language="russian") if x not in russian_stopwords]
    # print('Без стоп-слов:', source)

    # лемматизация
    morph = pymorphy2.MorphAnalyzer()
    source = [morph.parse(x)[0].normal_form for x in source]
    # print('С лемматизацией:', source)

    return source


def canonize_word(word):
    word = word.lower()
    spec_chars = string.punctuation + string.digits + '\n\r\t\xa0№«»—…„'
    word = "".join(ch for ch in word if ch not in spec_chars)
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0].normal_form

    return word


def delete_irrelevant_words(source, config):
    # 'supporting/irrelevant_words.txt'
    try:
        file = open(config, encoding='utf-8')
        line = file.read()
        irrelevant_words = line.split('\n')
        for word in irrelevant_words:
            source = source.replace(word, '')
    except IOError:
        raise IOError("File 'irrelevant_words' does not exist!")

    return source


def delete_tag(source):
    tags = ['</>', '</', '/>']
    for tag in tags:
        source = source.replace(tag, '')

    return source
