from email.mime import base
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import base_views, posting_views, comment_views

app_name = 'wyw'

urlpatterns = [
     path('profile/', base_views.profile, name='profile'),
    # path('',base_views.index, name='index'),
    # path('<int:posting_id>/', base_views.detail, name='detail'),
    # path('comment/create/<int:posting_id>/', posting_views.comment_create , name='comment_create'),
    # path('posting/create', posting_views.posting_create, name='posting_create'),
    # path('posting/modify/<int:posting_id>/', posting_views.posting_modify, name='posting_modify'),
    # path('posting/delete/<int:posting_id>/', comment_views.posting_delete, name='posting_delete'),
    # path('comment/modify/<int:comment_id>/', comment_views.comment_modify, name='comment_modify'),
    # path('comment/delete/<int:comment_id>/', comment_views.comment_delete, name='comment_delete'),
        # base_views.py
#     path('',
#          base_views.index, name='index'),
     path('posting/list/', base_views.index, name='index'),
    path('posting/list/<str:category_name>/', base_views.index, name='index'),

    path('posting/detail/<int:posting_id>/',
         base_views.detail, name='detail'),

    # question_views.py
     # path('posting/create/',
     #     posting_views.posting_create, name='posting_create'),
    path('posting/create/<str:category_name>/',
         posting_views.posting_create, name='posting_create'),
    path('posting/modify/<int:posting_id>/',
         posting_views.posting_modify, name='posting_modify'),
    path('posting/delete/<int:posting_id>/',
         posting_views.posting_delete, name='posting_delete'),
     # path('posting/craete/<str:category_name>/', posting_views.posting_create, name='posting_create'),


    # answer_views.py
    path('comment/create/<int:posting_id>/',
         comment_views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/',
         comment_views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/',
         comment_views.comment_delete, name='comment_delete'),

    path('posting/vote/<int:posting_id>/', posting_views.posting_vote, name='posting_vote'),
    path('posting/scrap/<int:posting_id>/', posting_views.posting_scrap, name='posting_scrap'),
     path('ranking/', base_views.ranking, name='ranking'),
     path('recommend/', base_views.recommend, name='recommend'),

    path('serializers/categorypost', base_views.CategoryPost.as_view()),
    path('serializers/categorypost/<int:pk>/', base_views.CategoryPost.as_view()),
    path('serializers/postingpost', base_views.PostingPost.as_view()),
    path('serializers/postingpost/<int:pk>/', base_views.PostingDetailPost.as_view()),
    path('serializers/commentpost', base_views.CommentPost.as_view()),
    path('serializers/commentpost/<int:pk>/', base_views.CommentDetailPost.as_view()),

     
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

