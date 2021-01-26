from anti.models import Law
from controllers.shingles import generate_list, generate_shingles
from supporting.preprocessing import generate_stopwords, canonize, cut_beginning, cut_end


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

    def make_shingles_equal_indexes(source, indexes):
        equal_indexes = []
        for index in range(len(source)):
            if index in indexes:
                for shingle_index in range(shingle_len):
                    if index + shingle_index not in equal_indexes:
                        equal_indexes.append(index + shingle_index)
        return equal_indexes

    def make_lsa_equal_indexes(source1, source2):
        equal_indexes = []
        for index in range(len(source1)):
            if source1[index] in source2:
                if index not in equal_indexes:
                    equal_indexes.append(index)
        return equal_indexes

    def get_string(source, shingles_equal_indexes, lsa_equal_indexes):
        result_str = ""
        for index in range(len(source)):
            if index in shingles_equal_indexes:
                current = "<mark>" + source[index] + "</mark> "
                if index in lsa_equal_indexes:
                    result_str += "<b>" + current + "</b>"
            else:
                if index in lsa_equal_indexes:
                    result_str += "<b>" + source[index] + "</b> "
                else:
                    result_str += source[index] + " "
        return result_str

    # canon_main
    shingles_equal_indexes_main = make_shingles_equal_indexes(canon_main_array, ind[1])
    lsa_equal_indexes_main = make_lsa_equal_indexes(canon_main_array, canon_cmp_array)
    result_str_main = get_string(canon_main_array, shingles_equal_indexes_main, lsa_equal_indexes_main)

    # canon_cmp
    shingles_equal_indexes_cmp = make_shingles_equal_indexes(canon_cmp_array, ind[0])
    lsa_equal_indexes_cmp = make_lsa_equal_indexes(canon_cmp_array, canon_main_array)
    result_str_cmp = get_string(canon_cmp_array, shingles_equal_indexes_cmp, lsa_equal_indexes_cmp)

    result = (result_str_main, result_str_cmp)

    return result


def main(shingle_len, main_text):
    russian_stopwords = generate_stopwords()

    cut_main_text = cut_end(cut_beginning(main_text))
    canon_main = canonize(cut_main_text, russian_stopwords)
    shingles_main = generate_shingles(canon_main, shingle_len)

    top = generate_list(shingles_main, shingle_len)
    top7 = []
    for i in range(7):
        top7.append([])
    for i in range(7):
        law = Law.objects.get(title=top[len(top) - 1 - i][0])
        canon_main_array = canonize(cut_main_text, russian_stopwords)
        canon_cmp_array = law.canon.split()
        result_str = compare_for_underline_canon(shingles_main, canon_main_array, canon_cmp_array, shingle_len)
        top7[0].append(top[len(top) - 1 - i][0])
        top7[1].append(top[len(top) - 1 - i][1])
        top7[2].append(result_str[0])
        top7[3].append(result_str[1])

    return top7
