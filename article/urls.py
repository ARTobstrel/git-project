from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from article.views import basic_one, template_two, template_three_simple, article, articles, addlike, addcomment, \
    keywords

urlpatterns = [
    url(r'^1/', basic_one),
    url(r'^2/', template_two),
    url(r'^3/', template_three_simple),
    url(r'^articles/all/$', articles),
    url(r'^articles/get/(?P<article_id>[0-9]+)', article),
    url(r'^article/addlike/(?P<article_id>[0-9]+)', addlike),
    url(r'^article/addcomment/(?P<article_id>[0-9]+)', addcomment),
    url(r'^page/(\d+)/$', articles),
    url(r'^$', articles),
    url(r'^keyword/(?P<id>\d+)/$', keywords),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)