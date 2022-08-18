from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import UserCreationForm
from account.models import User
from django.shortcuts import get_object_or_404, render, render, redirect
from wyw.models import Posting, Category, Comment
from django.views.generic import ListView
from itertools import chain
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UpdateProfileForm
from .models import Profile
from django.contrib.auth import get_user_model
from wyw.models import models

from rest_framework import generics

from .serializers import UserSerializer
from .serializers import ProfileSerializer



class UserPost(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfilePost(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer






def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        uploadimage = request.FILES.get("image")
        request.session['image'] = uploadimage


        form = UserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # profile2 = UpdateProfileForm(request.POST, request.FILES, instance=user)
            # profile.user = user
            # profile = Profile()
            # profile.user = user
            # profile.save()
            # profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile.user.profile)

            # if profile_form.is_valid():
            #     profile_form.save()
            #     login(request, user)
            #     return redirect('index')
            # profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile.user.profile)
            # profile_form.save()
            # profile.save()

            login(request, user)

            return redirect('index')
    else:
        form = UserCreationForm()
        profile_form = UpdateProfileForm()

    return render(request, 'account/signup.html', {'form': form, 'profile_form': profile_form})

def profile_base(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {'profile_user': user, 'user':User}
    return render(request, 'wyw/profile_scrap.html', context)

class ProfileObjectListView(ListView):
    """
    프로필 목록 추상 클래스 뷰
    """
    paginate_by = 10

    class Meta:
        abstract = True
    
    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        self.so = self.request.GET.get('so', 'recent')  # 정렬기준
        object_list = self.model.objects.filter(author=self.profile_user)
        # 정렬
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'profile_user': self.profile_user,
            'so': self.so
        })
        return context

class ProfileVoteListView(ProfileObjectListView):
    """
    작성한 댓글 목록
    """
    template_name = 'wyw/profile_scrap.html'
    
    def get_queryset(self):
        self.profile_user = get_object_or_404(User, pk=self.kwargs['user_id'])
        posting_list = self.profile_user.scrap_posting.all()

        _queryset = sorted(
            chain(posting_list),
            key=lambda obj: obj.create_date,
            reverse=True,
        )
        return _queryset
    
    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context.update({
            'profile_user': self.profile_user,
            # 'so': self.so
        })
        return context

# @login_required
# def profile(request):
#     form = UpdateProfileForm()
#     return render(request, 'wyw/profile.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('index')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)


    return render(request, 'wyw/profile.html', {'profile_form': profile_form })

@login_required
def follow(request, user_id):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_id)
        if person != request.user:
            # if request.user.followings.filter(pk=user_pk).exists():
            if person.followers.filter(pk=request.user.pk).exists():
                person.followers.remove(request.user)
            else:
                person.followers.add(request.user)
        # return redirect('wyw:index')
        return redirect('account:profile_scrap', user_id=user_id)
    return redirect('account:login')

