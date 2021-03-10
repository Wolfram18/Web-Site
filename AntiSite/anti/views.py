from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

from anti.models import Law
import controllers.shingles
import controllers.lsa
import controllers.compare
from controllers.search import get_law_by_title
from supporting.parser import get_pdf_fitz


def main(request):
    # import supporting.parser
    # supporting.parser.main()
    return render(request, "index.html")


def output(request):
    if 'my_range' in request.POST:
        shingle_len = int(request.POST['my_range'])
    else:
        shingle_len = 3
    if 'switch_1' in request.POST:
        value = request.POST['switch_1']
        if value == "on":
            format_out = True
        else:
            format_out = False
    else:
        format_out = False
    if request.method == 'POST':
        custom_file = request.FILES.get('customFile', False)
        if bool(custom_file):
            fs = FileSystemStorage()
            filename = fs.save(custom_file.name, custom_file)
            open_file = fs.open(filename, 'rb')
            # noinspection PyBroadException
            try:
                main_text = get_pdf_fitz(open_file)
                data = controllers.shingles.main(shingle_len, main_text, format_out)
                title = data[0]
                percent = data[1]
                result_str_main = data[2]
                result_str_cmp = data[3]
                return render(request, "index.html",
                              {"title": title, "percent": percent, "result_str_main": result_str_main,
                               "result_str_cmp": result_str_cmp, "shingle_len": shingle_len, "format_out": format_out})
            except Exception:
                return render(request, "index.html")
        else:
            return render(request, "index.html")
    else:
        return render(request, "index.html")


def semantic(request):
    return render(request, "semantic.html")


def semantic_output(request):
    if 'switch_1' in request.POST:
        value = request.POST['switch_1']
        if value == "on":
            format_out = True
        else:
            format_out = False
    else:
        format_out = False
    if request.method == 'POST':
        custom_file = request.FILES.get('customFile', False)
        if bool(custom_file):
            fs = FileSystemStorage()
            filename = fs.save(custom_file.name, custom_file)
            open_file = fs.open(filename, 'rb')
            # noinspection PyBroadException
            try:
                main_text = get_pdf_fitz(open_file)
                data = controllers.lsa.main(main_text, format_out)
                title = data[0]
                percent = data[1]
                result_str_main = data[2]
                result_str_cmp = data[3]
                return render(request, "semantic.html",
                              {"title": title, "percent": percent, "result_str_main": result_str_main,
                               "result_str_cmp": result_str_cmp, "format_out": format_out})
            except Exception:
                return render(request, "semantic.html")
        else:
            return render(request, "semantic.html")
    else:
        return render(request, "semantic.html")


def semantic_bar(request):
    #return {"iteration": controllers.lsa.get_iteration()}
    return HttpResponse(controllers.lsa.get_iteration())


def search(request):
    return render(request, "search.html")


def search_output(request):
    if 'find' in request.POST:
        law_index = request.POST['find']
        try:
            text = get_law_by_title(law_index)
            return render(request, "search.html", {"text": text})
        except Law.DoesNotExist:
            return render(request, "search.html", {"text": "Документ с таким индексом не найден"})
        except Law.MultipleObjectsReturned:
            return render(request, "search.html", {"text": "Ошибка: Несколько документов с таким индексом"})
    else:
        return render(request, "search.html")


def comparison(request):
    return render(request, "comparison.html")


def comparison_output(request):
    if 'my_range' in request.POST:
        shingle_len = int(request.POST['my_range'])
    else:
        shingle_len = 3
    if request.method == 'POST':
        custom_file = request.FILES.get('customFile', False)
        if bool(custom_file):
            fs = FileSystemStorage()
            filename = fs.save(custom_file.name, custom_file)
            open_file = fs.open(filename, 'rb')
            # noinspection PyBroadException
            try:
                main_text = get_pdf_fitz(open_file)
                data = controllers.compare.main(shingle_len, main_text)
                title = data[0]
                percent = data[1]
                result_str_main = data[2]
                result_str_cmp = data[3]
                return render(request, "comparison.html",
                              {"title": title, "percent": percent, "result_str_main": result_str_main,
                               "result_str_cmp": result_str_cmp, "shingle_len": shingle_len})
            except Exception:
                return render(request, "comparison.html")
        else:
            return render(request, "comparison.html")
    else:
        return render(request, "comparison.html")


def info(request):
    return render(request, "info.html")


def error404(request):
    return render(request, "error404.html")
