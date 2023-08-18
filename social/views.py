from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import ListView , UpdateView , DeleteView , DetailView
from .models import Post,Profile,FollowersCount
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm , ProfileUpdateForm , UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from itertools import chain 
import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.urls import reverse_lazy
# Create your views here.
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(author=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user) 

    for usernames in user_following_list:
        post_feed = Post.objects.filter(author__username=usernames).order_by('-date_posted')
        feed.append(post_feed)

 
    post_feed = list(chain(*feed))
    user_post_count = len(post_feed)

    all_users = User.objects.all()
    user_suggestion_list = [x for x in list(all_users) if (x not in list(user_following))]
    user_profile_list = []
    request_user = Profile.objects.get(author__username=request.user.username)
    for users in user_suggestion_list:
    	user_profile_list.append(Profile.objects.get(author__username=users))

    user_final_list = [x for x in list(user_profile_list) if x != request_user]
    random.shuffle(user_final_list) 

    return render(request, 'home.html', {'user_profile': user_profile, 'posts':post_feed , 'user_profile_list':user_final_list[:2], 'user_post_count':user_post_count})

#class PostListView(ListView):
#	meta = Post 
#	template_name = 'home.html'
#	context_object_name = 'posts'
#	ordering = ['-date_posted']

#	def get_queryset(self):
#		return Post.objects.order_by('-date_posted') 

@login_required 
def profile(request,pk):
	user_object = User.objects.get(username=pk)
	user_profile = Profile.objects.get(author=user_object)
	user_posts = Post.objects.filter(author=user_object)
	user_post_count = len(user_posts)
	follower = request.user.username
	user = pk
	if FollowersCount.objects.filter(follower=follower,user=user).first():
		button_text = 'Unfollow'
	else:
		button_text = 'Follow'

	user_followers = len(FollowersCount.objects.filter(user=pk))
	user_following = len(FollowersCount.objects.filter(follower=pk))


	context = {
	'user_object':user_object,
	'user_profile': user_profile,
	'user_posts' : user_posts,
	'user_post_count' : user_post_count,
	'button_text' : button_text,
	'user_followers' : user_followers,
	'user_following' : user_following

	}
	return render(request,'profile.html',context)  

def follow(request):
	if request.method == 'POST':
		follower = request.POST['follower']
		user = request.POST['user']

		if FollowersCount.objects.filter(follower=follower,user=user).first():
			delete_follower = FollowersCount.objects.get(follower=follower,user=user)
			delete_follower.delete()
			return redirect('/profile/'+user)
		else:
			new_follower = FollowersCount.objects.create(follower=follower,user=user)
			new_follower.save()
			return redirect('/profile/'+user)

	else:
		return redirect('/')

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('register')

	else:
		form = UserRegisterForm()

	return render(request, 'register.html', {'form':form})

@login_required
def profile_update(request):
	user_object = User.objects.get(username=request.user.username)
	user_profile = Profile.objects.get(author=user_object)
	user_posts = Post.objects.filter(author=user_object)
	user_post_count = len(user_posts)
	follower = request.user.username
	user = request.user.username
	if FollowersCount.objects.filter(follower=follower,user=user).first():
		button_text = 'Unfollow'
	else:
		button_text = 'Follow'

	user_followers = len(FollowersCount.objects.filter(user=request.user.username))
	user_following = len(FollowersCount.objects.filter(follower=request.user.username))


	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance = request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES , instance = request.user.profile)
		
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Your account has been updated!')

			return redirect('/')

	else:
		u_form = UserUpdateForm(instance = request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)

	context = {
	'u_form' : u_form, 
	'p_form' : p_form,
	'user_object':user_object,
	'user_profile': user_profile,
	'user_posts' : user_posts,
	'user_post_count' : user_post_count,
	'button_text' : button_text,
	'user_followers' : user_followers,
	'user_following' : user_following
	}

	return render(request, 'profile_update.html', context)

@login_required
def upload(request):
	if request.method == "POST":
		user = User.objects.get(username=request.user.username)
		image = request.FILES.get("post-img")
		caption = request.POST["caption"]

		new_post = Post.objects.create(author=user,image=image,caption=caption)
		new_post.save()
		messages.success(request,f'Your post has been uploaded!') 

		return redirect('/blog_home')

	else:
		return redirect('/blog_home')

@login_required
def search(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
        profile_lists_len = len(username_profile_list)
    return render(request, 'search.html', {'username_profile_list': username_profile_list,'profile_lists_len':profile_lists_len})



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = reverse_lazy("blog-home")
	template_name = 'post_confirm_delete.html'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
		

class PostDetailView(DetailView):
	model = Post 
	template_name = 'post_detail.html'

def home(request):
	return render(request,'index.html')
 
