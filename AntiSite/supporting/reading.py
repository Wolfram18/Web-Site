import sys
from anti.models import Law
import fitz


# pip install PyMuPDF


def get_all_laws():
    # noinspection PyBroadException
    try:
        return Law.objects.all()
    except Exception:
        print("Database access error!")
        # raise Exception("Database access error!")


def get_law_by_title(title):
    try:
        law = Law.objects.get(title=title)
        return law.text
    except Law.DoesNotExist:
        return "Law with such an index does not exist!"
    except Law.MultipleObjectsReturned:
        return "Several laws with such an index!"


def get_stopwords_config(config):
    try:
        file = open(config, encoding='utf-8')
        return file.read()
    except IOError:
        print("File 'stopwords' does not exist!")
        # raise IOError("Config file does not exist!")
        return "а б без более больше быть будто бы в вы вдруг ведь во вот впрочем все весь всегда всего г где " \
               "говорить д да даже два для до другой е если есть ещё еще ё ж же з за зачем здесь и из или иногда й к " \
               "как кажется какой когда конечно который кто куда л ли м между много может можно мой мы н ни нибудь " \
               "никогда ничего но ну не нет на над надо наконец нельзя о он она они об один опять от п при про по " \
               "под перед после потом потому почти р раз разве с сам свое своё себя сегодня сейчас сказать со совсем " \
               "т ты так там тем такой теперь то тогда тоже только том тот тут три у уж уже ф х хорошо хоть ц ч что " \
               "через чтоб чтобы чуть ш щ ъ ы ь э этот ю я ст n i fa "


def get_irrelevant_words_config(config):
    try:
        file = open(config, encoding='utf-8')
        return file.read()
    except IOError:
        print("File 'irrelevant_words' does not exist!")
        # raise IOError("Config file does not exist!")
        return "внесение изменение статья\nвнесении изменение\nвнести часть статья\n" \
               "соответствие часть статья\nизменение дополнить\nпункт следующий содержание\n" \
               "кодекс российский федерация\nсобрание законодательство российский федерация\n" \
               "законодательство российский федерация\nпрезидент российский федерация\n" \
               "российский федерация\nфедеральный закон\nпояснительный записка\n" \
               "административный правонарушение\nнормативный правовой акт"


def get_pdf_text(pdf_document):
    doc = fitz.open(pdf_document)
    count_page = doc.pageCount
    all_text = ''
    for i in range(count_page):
        page = doc.loadPage(i)
        text = page.getText("text")
        all_text += text
    return all_text


def updt(total, progress, prefix):
    barLength, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r{} [{}] {:.0f}% {}".format(prefix, "#" * block + "-" * (barLength - block),
                                         round(progress * 100, 0), status)
    sys.stdout.write(text)
    sys.stdout.flush()
