from anti.models import Law
from supporting.preprocessing import generate_stopwords, canonize, cut_end, cut_beginning, canonize_word, \
    delete_irrelevant_words

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


def generate_shingles(source, shingle_len):
    # алгоритм хэша
    import binascii
    out = []
    for i in range(len(source) - (shingle_len - 1)):
        out.append(binascii.crc32(' '.join([x for x in source[i:i + shingle_len]]).encode('utf-8')))

    return out


def compare_shingles(shingles_main, source):
    same = 0
    for i in range(len(shingles_main)):
        if shingles_main[i] in source:
            same = same + 1
    try:
        # можно расчитывать по-другому
        percent = float(same * 2) / float(len(shingles_main) + len(source)) * 100
    except ZeroDivisionError:
        percent = 0
    return int(percent)


# список "Название закона - процентаж"
def generate_list(shingles_main, shingle_len):
    files = Law.objects.all()
    top = []
    for i in range(files.count()):
        top.append([])
    for i in range(files.count()):
        set_iteration()
        cmp2 = generate_shingles(delete_irrelevant_words(files[i].canon).split(), shingle_len)
        top[i].append(files[i].title)
        top[i].append(compare_shingles(shingles_main, cmp2))
    top.sort(key=lambda x: x[1])

    return top


def compare_for_underline_canon(shingles_main, canon_main_array, canon_cmp_array, shingle_len):
    shingles_cmp = generate_shingles(canon_cmp_array, shingle_len)

    ind = []
    for i in range(2):
        ind.append([])

    # создаём массив индексов соответствия
    for i in range(len(shingles_main)):
        if shingles_main[i] in shingles_cmp:
            if shingles_cmp.count(shingles_main[i]) == 1:
                ind[0].append(shingles_cmp.index(shingles_main[i]))
                ind[1].append(i)
            else:
                for j in range(len(shingles_cmp)):
                    if shingles_main[i] == shingles_cmp[j]:
                        ind[0].append(j)
                        ind[1].append(i)

    def make_equal_indexes(source, indexes):
        equal_indexes = []
        for index in range(len(source)):
            if index in indexes:
                for shingle_index in range(shingle_len):
                    if index + shingle_index not in equal_indexes:
                        equal_indexes.append(index + shingle_index)
        return equal_indexes

    def get_string(source, equal_indexes):
        result_str = ""
        for index in range(len(source)):
            if index in equal_indexes:
                result_str += "<mark>" + source[index] + "</mark> "
            else:
                result_str += source[index] + " "
        return result_str

    # при совпадении для canon_main
    equal_indexes_main = make_equal_indexes(canon_main_array, ind[1])
    result_str_main = get_string(canon_main_array, equal_indexes_main)

    # при совпадении для canon_cmp
    equal_indexes_cmp = make_equal_indexes(canon_cmp_array, ind[0])
    result_str_cmp = get_string(canon_cmp_array, equal_indexes_cmp)

    result = (result_str_main, result_str_cmp)

    return result


# не по длине шингла, а по совпадениям
def compare_for_underline_text(shingles_main, canon_main_array, main_text_array, canon_cmp_array, text_cmp,
                               shingle_len, russian_stopwords):
    shingles_cmp = generate_shingles(canon_cmp_array, shingle_len)

    ind = []
    for i in range(2):
        ind.append([])

    # создаём массив индексов соответствия
    for i in range(len(shingles_main)):
        if shingles_main[i] in shingles_cmp:
            if shingles_cmp.count(shingles_main[i]) == 1:
                ind[0].append(shingles_cmp.index(shingles_main[i]))
                ind[1].append(i)
            else:
                for j in range(len(shingles_cmp)):
                    if shingles_main[i] == shingles_cmp[j]:
                        ind[0].append(j)
                        ind[1].append(i)

    def make_equal_words(source, indexes):
        equal_words = []
        for index in range(len(source)):
            if index in indexes:
                for shingle_index in range(shingle_len):
                    if source[index + shingle_index] not in equal_words:
                        equal_words.append(source[index + shingle_index])
        return equal_words

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
    equal_words_main = make_equal_words(canon_main_array, ind[1])
    result_str_main = get_string(main_text_array, equal_words_main)

    # при совпадении делаем <mark> для canon_cmp
    equal_words_cmp = make_equal_words(canon_cmp_array, ind[0])
    text_cmp_array = cut_end(cut_beginning(text_cmp)).split()
    result_str_cmp = get_string(text_cmp_array, equal_words_cmp)

    result = (result_str_main, result_str_cmp)

    return result


def main(shingle_len, main_text, format_out):
    delete_iteration()
    russian_stopwords = generate_stopwords()

    cut_main_text = cut_end(cut_beginning(main_text))
    if format_out:
        main_text_array = cut_main_text.split()
    canon_main = canonize(cut_main_text, russian_stopwords)
    shingles_main = generate_shingles(canon_main, shingle_len)

    top = generate_list(shingles_main, shingle_len)
    top7 = []
    for i in range(7):
        top7.append([])
    for i in range(7):
        set_iteration()
        law = Law.objects.get(title=top[len(top) - 1 - i][0])
        canon_main_array = canonize(cut_main_text, russian_stopwords)
        canon_cmp_array = delete_irrelevant_words(law.canon).split()
        if format_out:
            text_cmp = law.text
            result_str = compare_for_underline_text(shingles_main, canon_main_array, main_text_array, canon_cmp_array,
                                                    text_cmp, shingle_len, russian_stopwords)
        else:
            result_str = compare_for_underline_canon(shingles_main, canon_main_array, canon_cmp_array, shingle_len)

        top7[0].append(top[len(top) - 1 - i][0])
        top7[1].append(top[len(top) - 1 - i][1])
        top7[2].append(result_str[0])
        top7[3].append(result_str[1])

    return top7
