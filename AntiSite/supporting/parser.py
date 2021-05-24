import os
from os import path
from os import listdir
import requests
from bs4 import BeautifulSoup
# import lxml
import fitz
# pip install PyMuPDF
import shutil
from anti.models import Law
from supporting.preprocessing import *


# возвращает html-код страницы в виде текста
def get_html(url):
    r = requests.get(url)
    return r.text


# возвращает количество страниц для парсинга
def get_total_count_of_pages(html):
    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('ul', class_='pagination').find_all('a', class_='merge_pagination')[-2].get('href')
    total_pages = pages.split('=')[-1]

    return int(total_pages)


# возвращает список ссылок на страницы законов
def get_bills_links_list(html):
    bills = []
    soup = BeautifulSoup(html, 'lxml')
    first = soup.find('div', class_='obj_item click_open first_item')
    dco = 'https://sozd.duma.gov.ru' + first.get('data-clickopen')
    bills.append(str(dco))
    ads = soup.find_all('div', class_='obj_item click_open')

    for ad in ads:
        dco = 'https://sozd.duma.gov.ru' + ad.get('data-clickopen')
        bills.append(str(dco))

    last = soup.find('div', class_='obj_item click_open last_item')
    dco = 'https://sozd.duma.gov.ru' + last.get('data-clickopen')
    bills.append(str(dco))

    return bills


def get_file(url):
    r = requests.get(url, stream=True)
    return r


# возвращает имя для pdf-файла
def get_file_name(url):
    name = url.split('/')[-1]
    return name


# возвращает ссылку для скачивая pdf-файла
def get_download_link(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('table', class_='table table-hover table-striped borderless fs13px').find_all('tr')[-1].\
        find('div', class_='opch_r').find('a').get('href')

    return ads


# сохраняет pdf-файл
def save_pdf(name, file_object, dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    my_path = os.path.abspath(dir_)
    name = os.path.join(my_path, name)
    with open(name + '.pdf', 'bw') as f:
        for chunk in file_object.iter_content(8192):
            f.write(chunk)


def get_file_names_from_dir(my_path):
    file_names = []
    for file_name in listdir(my_path):
        full_path = path.join(my_path, file_name)
        if path.isfile(full_path):
            file_names.append(file_name)
    print(file_names)

    return file_names


def get_pdf_fitz(pdf_document):
    doc = fitz.open(pdf_document)
    count_page = doc.pageCount
    # print("Количество страниц: %i" % count_page)
    all_text = ''
    for i in range(count_page):
        page = doc.loadPage(i)
        text = page.getText("text")
        all_text += text

    return all_text


def remove_file(my_path):
    if os.path.isfile(my_path):
        os.remove(my_path)


def remove_contents(my_path):
    for c in os.listdir(my_path):
        full_path = os.path.join(my_path, c)
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)


def check_updates(base_url, str_beg, str_end):
    russian_stopwords = generate_stopwords('supporting/stopwords.txt')

    my_path = "supporting/data/"
    # main_url = base_url + '1'
    # total_pages = get_total_count_of_pages(get_html(main_url))

    flag = True
    for i in range(str_beg, str_end):
        if flag:
            url_gen = base_url + str(i)
            html = get_html(url_gen)
            bills = get_bills_links_list(html)
            for j in range(0, len(get_bills_links_list(html))):
                html2 = get_html(bills[j])
                gdl = get_download_link(html2)
                title = get_file_name(bills[j])
                try:
                    Law.objects.get(title=title)
                    flag = False
                    break
                except Law.DoesNotExist:
                    if gdl is not None:
                        save_pdf(title, get_file("https://sozd.duma.gov.ru" + gdl), my_path)
                    else:
                        continue
                except Law.MultipleObjectsReturned:
                    print("Ошибка: Несколько документов с индексом", title)
        else:
            break

    file_names = get_file_names_from_dir(my_path)
    for k in range(0, len(file_names)):
        text = get_pdf_fitz(my_path + file_names[k])
        canon_array = canonize(cut_end(cut_beginning(text)), russian_stopwords)
        canon_text = ""
        for z in range(0, len(canon_array)):
            canon_text += canon_array[z] + " "
        canon_text = delete_irrelevant_words(canon_text, 'supporting/irrelevant_words.txt')
        try:
            Law.objects.get(title=file_names[k].rstrip('.pdf'))
        except Law.DoesNotExist:
            Law.objects.create(title=file_names[k].rstrip('.pdf'), text=text, canon=canon_text)
        except Law.MultipleObjectsReturned:
            pass

    remove_contents(my_path)


def main(base_url, str_beg, str_end):
    russian_stopwords = generate_stopwords('supporting/stopwords.txt')

    my_path = "supporting/data/"
    # main_url = base_url + '1'
    # total_pages = get_total_count_of_pages(get_html(main_url))

    for i in range(str_beg, str_end):
        url_gen = base_url + str(i)
        html = get_html(url_gen)
        bills = get_bills_links_list(html)
        for j in range(0, len(get_bills_links_list(html))):
            html2 = get_html(bills[j])
            gdl = get_download_link(html2)
            if gdl is not None:
                save_pdf(get_file_name(bills[j]), get_file("https://sozd.duma.gov.ru" + gdl), my_path)
            else:
                continue

        file_names = get_file_names_from_dir(my_path)
        for k in range(0, len(file_names)):
            text = get_pdf_fitz(my_path + file_names[k])
            text = delete_tag(text)
            canon_array = canonize(cut_end(cut_beginning(text)), russian_stopwords)
            canon_text = ""
            for z in range(0, len(canon_array)):
                canon_text += canon_array[z] + " "
            canon_text = delete_irrelevant_words(canon_text, 'supporting/irrelevant_words.txt')
            # get_or_create()
            # Law.objects.filter(title=title).update(canon=canon_text)
            try:
                Law.objects.get(title=file_names[k].rstrip('.pdf'))
            except Law.DoesNotExist:
                Law.objects.create(title=file_names[k].rstrip('.pdf'), text=text, canon=canon_text)
            except Law.MultipleObjectsReturned:
                pass

        remove_contents(my_path)


if __name__ == '__main__':
    main()
