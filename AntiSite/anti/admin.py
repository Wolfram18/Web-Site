from django.contrib import admin
from anti.models import Law


class LawAdmin(admin.ModelAdmin):
    pass


admin.site.register(Law, LawAdmin)
