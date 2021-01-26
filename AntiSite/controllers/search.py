from anti.models import Law


def get_law_by_title(title):
    law = Law.objects.get(title=title)
    return law.text
