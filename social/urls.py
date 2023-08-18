from django.urls import path
from . import views
#from .views import PostListView
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from .views import(
	PostDeleteView,
	PostDetailView
	)

urlpatterns = [
	#path('', PostListView.as_view(), name='blog-home'),
	path('', views.home, name='home'),
	path('blog_home', views.index, name='blog-home'),
	path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name = 'logout'),
	path('profile/<str:pk>',views.profile, name='profile'),
	path('follow/',views.follow, name='follow'),
	path('register/', views.register, name='register'),
	path('profile_update/',views.profile_update, name='profile_update'),
	path('upload/',views.upload, name='upload'),
	path('search/', views.search, name='search'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail')
]

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

