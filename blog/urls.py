from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = ([
    path('admin/', admin.site.urls),
    path('index/',Index,name="index"),
    path('',Home,name="home"),
    path('blog/',Blogs,name="blog"),
    path('post_detail<int:pk>/',Post_detail,name="post_detail"),
    path('post_form/',Post_form,name="post_form"),
    path('post_blog/',Post_blog,name="post_blog"),
    path('gallery/',Gallery,name="gallery"),
    path('video/',Video,name="video"),
    path('signin/',Signin,name="signin"),
    path('login/',Login,name="login"),
    path('logout/',Logout,name="logout"),
    path('blogs/', public_blog, name='blogs'),
    path('Delete_comment<int:comment_id>/',Delete_comment,name="delete_comment"),
    path('like/<int:pk>/',Like_post, name='like_post'),
    path('comment/<int:pk>/', add_comment, name='add_comment'),
    path('profile/',Profile,name="profile"),
    path('edit_profile/',Edit_profile,name="edit_profile"),
    path('delete_post/<int:pk>/',Delete_post,name="delete_post"),
    path('about/',About,name="about"),
    path('contact/',Contact,name="contact")

]
 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
