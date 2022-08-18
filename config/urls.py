from django.contrib import admin
from django.urls import path, include
from wyw.views import base_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('whatyourweb/',include('wyw.urls')),
    path('account/',include('account.urls'),),
    path('',base_views.index, name='index'),
    path('summernote/', include('django_summernote.urls')),
	re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)