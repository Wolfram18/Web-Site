# nltk.download()
import string
import pymorphy2


# вырезать до ПОСТАНОВЛЕНИЕ и ФЕДЕРАЛЬНЫЙ ЗАКОН
def cut_beginning(source):
    if source.find("ПОСТАНОВЛЕНИЕ") != -1:
        index_p = source.find("ПОСТАНОВЛЕНИЕ") + len("ПОСТАНОВЛЕНИЕ")
    elif source.find("П О С Т А Н О В Л Е Н И Е") != -1:
        index_p = source.find("П О С Т А Н О В Л Е Н И Е") + len("П О С Т А Н О В Л Е Н И Е")
    else:
        index_p = 0

    if source.find("ФЕДЕРАЛЬНЫЙ ЗАКОН") != -1:
        index_f = source.find("ФЕДЕРАЛЬНЫЙ ЗАКОН") + len("ФЕДЕРАЛЬНЫЙ ЗАКОН")
    elif source.find("Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н") != -1:
        index_f = source.find("Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н") + len("Ф Е Д Е Р А Л Ь Н Ы Й З А К О Н")
    else:
        index_f = 0

    if index_p == 0:
        return source[index_f:]
    elif index_f == 0:
        return source[index_p:]
    elif index_p > index_f:
        return source[index_f:]
    elif index_p < index_f:
        return source[index_p:]
    else:
        return source


# вырезать после ПЕРЕЧЕНЬ и ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ
def cut_end(source):
    if source.find("ПЕРЕЧЕНЬ") != -1:
        source = source[:source.find("ПЕРЕЧЕНЬ")]
    elif source.find("П Е Р Е Ч Е Н Ь") != -1:
        source = source[:source.find("П Е Р Е Ч Е Н Ь")]
    elif source.find("Перечень федеральных законов") != -1:
        source = source[:source.find("Перечень федеральных законов")]

    if source.find("ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ") != -1:
        source = source[:source.find("ФИНАНСОВО-ЭКОНОМИЧЕСКОЕ ОБОСНОВАНИЕ")]

    return source


# Добавить канонизацию
def generate_stopwords():
    # готовый словарь
    from nltk.corpus import stopwords
    russian_stopwords = stopwords.words("russian")

    # наш словарь
    line = open('supporting/stopwords.txt', encoding='utf-8').read()
    words = line.split()
    russian_stopwords.extend(words)

    return russian_stopwords


def canonize(source, russian_stopwords):
    # приводим к нижнему регистру
    source = source.lower()
    # print('Нижний регистр:', source)

    # удаляем пунктуацию и цифры
    spec_chars = string.punctuation + string.digits + '\n\r\t\xa0№«»—…„'
    source = "".join([ch for ch in source if ch not in spec_chars])
    # print('Без символов:', source)

    # разбиваем и удаляем стоп слова
    from nltk.tokenize import word_tokenize
    source = [x for x in word_tokenize(source, language="russian") if x not in russian_stopwords]
    # print('Без стоп-слов:', source)

    # лемматизация
    morph = pymorphy2.MorphAnalyzer()
    source = [morph.parse(x)[0].normal_form for x in source]
    # print('С лемматизацией:', source)

    return source


def delete_irrelevant_words(source):
    line = open('supporting/irrelevant_words.txt', encoding='utf-8').read()
    irrelevant_words = line.split('\n')
    for word in irrelevant_words:
        source = source.replace(word, '')

    return source


def canonize_word(word):
    word = word.lower()
    spec_chars = string.punctuation + string.digits + '\n\r\t\xa0№«»—…„'
    word = "".join(ch for ch in word if ch not in spec_chars)
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0].normal_form

    return word