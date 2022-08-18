from django.contrib import admin
from .models import Posting
from .models import Comment
from .models import Category
from django_summernote.admin import SummernoteModelAdminMixin


# # class PostingAdmin(admin.ModelAdmin):
# #     search_fields = ['subject'],
# #     summernote_fields = ('content',)
# @admin.register(Posting)
# class PostingAdmin(SummernoteModelAdminMixin, admin.ModelAdmin):
#     summernote_fields = ('contents',)
#     list_display = (
#         'title',
#         'contents',
#         'writer',
#         'board_name',
#         'hits',
#         'write_dttm',
#         'update_dttm',
#     )
#     list_display_links = list_display
#     search_fields = ['subject'],
#     # summernote_fields = ('content',)


# # class PostAdmin(SummernoteModelAdmin):
# #     summernote_fields = ('content',)

# admin.site.register(Posting, PostingAdmin)

class PostingAdmin(SummernoteModelAdminMixin ,admin.ModelAdmin):
    search_fields = ['subject']

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['subject']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['subject']


admin.site.register(Posting, PostingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
