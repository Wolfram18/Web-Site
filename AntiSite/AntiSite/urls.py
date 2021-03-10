from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from AntiSite import settings
from anti import views

urlpatterns = [
    path('', views.main, name="main"),
    path('main', views.main),
    path('main.html', views.main),
    re_path(r'^main/', views.main),
    # re_path(r'^main', views.m404),
    path('output', views.output, name="output"),
    re_path(r'^output/', views.output),
    # re_path(r'^output', views.m404),

    path('semantic', views.semantic, name="semantic"),
    path('semantic.html', views.semantic),
    re_path(r'^semantic/', views.semantic),
    path('semantic_output', views.semantic_output, name="semantic_output"),
    re_path(r'^semantic_output/', views.semantic_output),
    url(r'^semantic_bar/$', views.semantic_bar),

    path('comparison', views.comparison, name="comparison"),
    path('comparison.html', views.comparison),
    re_path(r'^comparison/', views.comparison),
    path('comparison_output', views.comparison_output, name="comparison_output"),
    re_path(r'^comparison_output/', views.comparison_output),

    path('search', views.search, name="search"),
    path('search.html', views.search),
    re_path(r'^search/', views.search),
    path('search_output', views.search_output, name="search_output"),
    re_path(r'^search_output/', views.search_output),

    path('info', views.info, name="info"),
    path('info.html', views.info),
    re_path(r'^info/', views.info),

    path('admin', admin.site.urls),
    path('admin/', admin.site.urls),
    re_path(r'^', views.error404),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
