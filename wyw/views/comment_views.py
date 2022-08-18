from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, render, redirect
from django.utils import timezone
from django.db.models import Q


from ..forms import CommentForm
from ..models import Posting, Comment

@login_required(login_url='common:login')
def comment_create(request, posting_id):
    """
    댓글 등록
    """

    posting = get_object_or_404(Posting, pk=posting_id)
    # comment_list = Comment.objects.filter(Comment, posting_id = posting.pk)
    comment_list = Comment.objects.filter(Q(Posting = posting) & Q(author = request.user) )


    if (comment_list):
        messages.error(request, '이미 댓글을 작성하셨습니다.')
        return redirect('wyw:detail', posting_id=posting_id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user # author 속성에 로그인 계정 저장
        comment.create_date = timezone.now()
        comment.Posting = posting
        comment.save()
        return redirect('wyw:detail', posting_id=posting.id)
    else:
        form = CommentForm()
    context = {'posting':posting, 'form':form}
    return render(request,'wyw/posting_detail.html', context)

@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('wyw:detail', posting_id=comment.Posting.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('wyw:detail', posting_id=comment.Posting.id)
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'wyw/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('wyw:detail', posting_id=comment.Posting.id)
