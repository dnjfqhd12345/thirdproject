from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, render, redirect
from django.utils import timezone

from ..forms import PostingForm
from ..models import Posting, Category, Comment
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import dload
import os
import requests

@login_required(login_url='account:login')
def posting_create(request, category_name):
    category = Category.objects.get(name=category_name)
    if request.method == 'POST':
        form = PostingForm(request.POST)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.author = request.user # author 속성에 로그인 계정 저장
            posting.author_avatar = request.user.profile
            posting.create_date = timezone.now()

            posting.category = category

            response = requests.get(request.POST.get("logo", ""))

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                image = soup.select_one('meta[property="og:image"]')['content']




            posting.logo = image
# 크롬에서 가져오고 싶은 이미지 오른쪽 클릭
# 검사 -> 개발자 도구에서의 선택된 부분을 오린쪽 클릭
# copy -> copy selector 를 하여 복사된 정보에서 중복을 삭제
 
            # src = thumbnails["content"]    # 가져온 태그 정보중에 src만 가져옴
            # posting.logo = dload.save(image, f'C:\Django\whatyourweb\wyw\images/333.jpg')    # 설정한 경로로 jpg파일로 다운로드
            # driver.quit() # 끝나면 닫아주기
            # path='C:\Django\whatyourweb\wyw\images'
            # img_list = os.listdir(path)
            # posting.logo = img_list
            posting.save()
            return redirect('wyw:detail', posting_id=posting.id)
    else:
        form = PostingForm()

    context = {'form': form, 'category': category,}
    return render(request, 'wyw/posting_form.html', context)

@login_required(login_url='account:login')
def posting_modify(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.user != posting.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('wyw:detail', posting_id=posting.id)
    if request.method == "POST":
        form = PostingForm(request.POST, instance=posting)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.modify_date = timezone.now()  # 수정일시 저장
            response = requests.get(request.POST.get("logo", ""))

            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                image = soup.select_one('meta[property="og:image"]')['content']




            posting.logo = image

            posting.save()
            return redirect('wyw:detail', posting_id=posting.id)
    else:
        form = PostingForm(instance=posting)
    context = {'form': form}
    return render(request, 'wyw/posting_form.html', context)

@login_required(login_url='account:login')
def posting_delete(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.user != posting.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('wyw:detail', posting_id=posting.id)
    posting.delete()
    return redirect('wyw:index')

@login_required(login_url='account:login')
def posting_vote(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    if request.user == posting.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        posting.voter.add(request.user)
    return redirect('wyw:detail', posting_id=posting.id)

@login_required(login_url='account:login')
def posting_scrap(request, posting_id):
    posting = get_object_or_404(Posting, pk=posting_id)
    if posting.scraper.filter(id=request.user.id).exists():
        posting.scraper.remove(request.user)  # 이미 추가되어 있다면 삭제한다.
        posting.scrap_counter -= 1
        posting.save()  # save가 있어야 반영된다.
    else:
        posting.scraper.add(request.user)  # 포스팅의 likeUser에 user를 더한다.
        posting.scrap_counter += 1
        posting.save()
    return redirect('wyw:detail', posting_id=posting_id)

