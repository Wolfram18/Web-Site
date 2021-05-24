from collections import Counter
import operator
import math

from anti.models import Law
from supporting.preprocessing import generate_stopwords, canonize, cut_end, cut_beginning, canonize_word

COUNT_OUTPUT = 7
iteration = 0


def set_iteration():
    global iteration
    iteration = iteration + 1


def delete_iteration():
    global iteration
    iteration = 0


def get_iteration():
    global iteration
    return iteration


# словарь слов (ключ - слово, значение - индекс в векторе)
def build_terms(documents):
    terms = {}
    current_index = 0
    for doc in documents:
        set_iteration()
        for word in doc.split():
            if word not in terms:
                terms[word] = current_index
                current_index += 1

    return terms


# отношение числа вхождений слова к общему числу слов документа
def make_tf(document, terms):
    words = document.split()
    total_words = len(words)
    # подсчет количества повторений
    # (ключ - слово, значение - его повторы)
    doc_counter = Counter(words)

    for word in doc_counter:
        # Можно и не делить, а оставить как есть, с частотой
        doc_counter[word] /= total_words

    # сопоставление tf и индекса слова в векторе
    tfs = [0 for _ in range(len(terms))]
    for term, index in terms.items():
        tfs[index] = doc_counter[term]

    return tfs


# инверсия частоты, с которой слово встречается в документах коллекции
def make_idf(documents, terms):
    total_docs = len(documents)
    idfs = [0 for _ in range(len(terms))]
    for word, index in terms.items():
        docs_with_word = _count_docs_with_word(word, documents)
        # Основание логарифма не имеет значения
        # Без отрицательных значений, только положительные
        idf = 1 + math.log10(total_docs / docs_with_word)
        # сопоставление idf и индекса слова в векторе
        idfs[index] = idf

    return idfs


def _count_docs_with_word(word, docs):
    counter = 1
    for doc in docs:
        if word in doc:
            counter += 1
    return counter


# мера tf-idf - это произведение двух сомножителей
def build_tf_idf(documents, document, terms):
    doc_tf = make_tf(document, terms)
    doc_idf = make_idf(documents, terms)

    return _merge_td_idf(doc_tf, doc_idf, terms)


def _merge_td_idf(tf, idf, terms):
    return [tf[i] * idf[i] for i in range(len(terms))]


def cosine_similarity(vec1, vec2):
    def dot_product2(v1, v2):
        return sum(map(operator.mul, v1, v2))

    def vector_cos5(v1, v2):
        prod = dot_product2(v1, v2)
        len1 = math.sqrt(dot_product2(v1, v1))
        len2 = math.sqrt(dot_product2(v2, v2))
        try:
            res = prod / (len1 * len2)
        except ZeroDivisionError:
            res = 0
        return res

    return vector_cos5(vec1, vec2)


# список "Название закона - косинусное расстояние"
def generate_list(canon_main, files):
    documents = []
    titles = []
    for i in range(files.count()):
        documents.append(files[i].canon)
        titles.append(files[i].title)
    # словарь
    terms = build_terms(documents)
    # print(terms.keys())

    # матрица вхождения отдельных слов в документы
    tf_idf_total = []
    for document in documents:
        set_iteration()
        tf_idf_total.append(build_tf_idf(documents, document, terms))
    # for doc_rating in tf_idf_total:
    #    print(doc_rating)

    # сравниваем исходные вектора с новым
    top = []
    for i in range(files.count()):
        top.append([])
    query_tfidf = build_tf_idf(documents, canon_main, terms)
    for index, document in enumerate(tf_idf_total):
        # print("Similarity with DOC", titles[index], "=", cosine_similarity(query_tfidf, document))
        set_iteration()
        top[index].append(titles[index])
        top[index].append(cosine_similarity(query_tfidf, document))
    top.sort(key=lambda x: x[1])

    return top


def _make_equal_words(source1, source2):
    equal_words = []
    for i in range(len(source1)):
        if source1[i] in source2:
            equal_words.append(source1[i])
    return equal_words


def compare_for_underline_canon(canon_main_array, canon_cmp_array):
    def get_string(source, equal_words):
        result_str = ""
        for word in source:
            if word in equal_words:
                result_str += "<mark>" + word + "</mark> "
            else:
                result_str += word + " "
        return result_str

    # при совпадении делаем <mark> для canon_main
    equal_words_main = _make_equal_words(canon_main_array, canon_cmp_array)
    result_str_main = get_string(canon_main_array, equal_words_main)

    # при совпадении делаем капс <mark> canon_cmp
    equal_words_cmp = _make_equal_words(canon_cmp_array, canon_main_array)
    result_str_cmp = get_string(canon_cmp_array, equal_words_cmp)

    result = (result_str_main, result_str_cmp)

    return result


def compare_for_underline_text(canon_main_array, main_text_array, canon_cmp_array, text_cmp, russian_stopwords):
    def get_string(source, equal_words):
        result_str = ""
        for word in source:
            canon_word = canonize_word(word)
            if canon_word in equal_words and canon_word not in russian_stopwords:
                result_str += "<mark>" + word + "</mark> "
            else:
                result_str += word + " "
        return result_str

    # при совпадении делаем <mark> для canon_main
    equal_words_main = _make_equal_words(canon_main_array, canon_cmp_array)
    result_str_main = get_string(main_text_array, equal_words_main)

    # при совпадении делаем <mark> для canon_cmp
    equal_words_cmp = _make_equal_words(canon_cmp_array, canon_main_array)
    text_cmp_array = cut_end(cut_beginning(text_cmp)).split()
    result_str_cmp = get_string(text_cmp_array, equal_words_cmp)

    result = (result_str_main, result_str_cmp)

    return result


def main(main_text, format_out, files):
    delete_iteration()
    russian_stopwords = generate_stopwords('supporting/stopwords.txt')

    canon_main_array = canonize(cut_end(cut_beginning(main_text)), russian_stopwords)
    canon_main = ""
    for z in range(0, len(canon_main_array)):
        canon_main += canon_main_array[z] + " "
    if format_out:
        main_text_array = cut_end(cut_beginning(main_text)).split()

    top = generate_list(canon_main, files)
    top_count = []
    for i in range(COUNT_OUTPUT):
        top_count.append([])
    for i in range(COUNT_OUTPUT):
        set_iteration()
        law = Law.objects.get(title=top[len(top) - 1 - i][0])
        canon_cmp_array = law.canon.split()
        if format_out:
            text_cmp = law.text
            result_str = compare_for_underline_text(canon_main_array, main_text_array, canon_cmp_array, text_cmp,
                                                    russian_stopwords)
        else:
            result_str = compare_for_underline_canon(canon_main_array, canon_cmp_array)

        top_count[0].append(top[len(top) - 1 - i][0])
        top_count[1].append(float("{0:.2f}".format(top[len(top) - 1 - i][1])))
        top_count[2].append(result_str[0])
        top_count[3].append(result_str[1])

    return top_count
