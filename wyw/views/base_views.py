from unicodedata import category, name
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render, render, redirect
from django.contrib.auth.decorators import login_required

from ..forms import CommentForm
from ..models import Posting # 부모 디렉토리
from ..models import Comment
from ..models import Category
from account.models import User
from django.db.models import Avg
from ..serializers import CategorySerializer
from ..serializers import PostingSerializer
from ..serializers import CommentSerializer
from rest_framework import generics

class CategoryPost(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostingPost(generics.ListCreateAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

class PostingDetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

class CommentPost(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


def index(request, category_name='backend'):
    category = Category.objects.get(name=category_name)
    """
    게시글 목록 출력
    """

    # 입력 인자
    page = request.GET.get('page','1')
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recommend')  # 정렬기준
    cat = request.GET.get('category')  # 정렬기준


    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)

    # # 조회
    posting_list = Posting.objects.filter(category=category)



            # 정렬
    if so == 'recommend':
        posting_list = Posting.objects.filter(category=category).annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        posting_list = Posting.objects.filter(category=category).annotate(num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:  # recent
        posting_list = Posting.objects.filter(category=category).order_by('-create_date')

    if kw:
        posting_list = posting_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__name__icontains=kw) |  # 질문 글쓴이검색
            Q(comment__author__name__icontains=kw)  # 답글 글쓴이검색
        ).distinct()


    # 페이징 처리
    paginator = Paginator(posting_list, 10) # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)


    context = {'posting_list' : page_obj, 'page':page, 'kw':kw,'category_list':category_list,'category':category, 'so':so, 'user':request.user}
    return render(request, 'wyw/posting_list.html', context)

def detail(request, posting_id):
    """
    Posting 내용 출력
    """
    posting = get_object_or_404(Posting, pk=posting_id)
    ratings = Comment.objects.filter(Posting=posting)
    rated = 1
    
    for rating in ratings:
        if request.user == rating.author:
            rated = rating
    rating_form = CommentForm()

    sum = Comment.objects.filter(Posting=posting).aggregate(Avg('score'))
    if sum['score__avg']:
        avg_score = round(sum['score__avg'],2)
    else:
        avg_score = 0

    posting.user_Rating = avg_score
    posting.save()

    context = {'posting':posting,'rating_form':rating_form, 'avg_score':avg_score }
    return render(request, 'wyw/posting_detail.html', context)

def profile(request):
    context = {'user': request.user}
    return render(request, 'wyw/profile.html', context)

def ranking(request):
    user_list = User.objects.all().order_by('-followers')
    return render(request, 'wyw/ranking.html', {'allUser':user_list})

@login_required(login_url='account:login')
def recommend(request):
    category = Category.objects.all()
    # fav1 = request.user.favorites_1
    # fav2 = request.user.favorites_2
    category_list_1 = Category.objects.filter(description__startswith = request.user.favorites_1)
    category_list_2 = Category.objects.filter(description__startswith = request.user.favorites_2)

    posting_list_1 = Posting.objects.filter(category__in = category_list_1)
    posting_list_2 = Posting.objects.filter(category__in = category_list_2)
    posting_list_1 = posting_list_1.annotate(num_voter=Count('voter')).order_by('-num_voter')
    posting_list_2 = posting_list_2.annotate(num_voter=Count('voter')).order_by('-num_voter')


    all_list = [posting_list_1, posting_list_2]




    category_list = Category.objects.all()

    context = {'posting_list_1':posting_list_1, 'posting_list_2':posting_list_2, 'category_list':category_list, 'category':category, 'user': request.user, 'all_list' : all_list}

    return render(request, 'wyw/recommend_site.html',context)