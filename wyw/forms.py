from django import forms
from wyw.models import Posting, Comment
from django_summernote.widgets import SummernoteWidget

class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = ['subject', 'content']
        widgets = {'content': SummernoteWidget(), }
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class':'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }
        labels = {
            'subject':'제목',
            'content':'내용',
        }

    # def clean(self):
    #     cleaned_data = super().clean()

    #     title = cleaned_data.get('title', '')
    #     contents = cleaned_data.get('contents', '')
    #     board_name = cleaned_data.get('board_name', '백엔드')

    #     if title == '':
    #         self.add_error('title', '글 제목을 입력하세요.')
    #     elif contents == '':
    #         self.add_error('contents', '글 내용을 입력하세요. ')
    #     else:
    #         self.title = title
    #         self.contents = contents
    #         self.board_name = board_name

POINT_CHOICES = (
    ('1' , 1),
    ('2' , 2),
    ('3' , 3),
    ('4' , 4),
    ('5' , 5),
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'score']
        labels = {
            'content':'댓글내용',
            'point':'평점',
        }
        widgets = {
            'restaurant' : forms.HiddenInput(),
            'score' : forms.Select(choices=POINT_CHOICES)
        }
