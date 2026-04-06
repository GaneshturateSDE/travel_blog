from django.db import models
from django.contrib.auth.models import User
import os.path

# Create your own models here.

class TravelPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',default=1)
    title = models.CharField(max_length=250)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    video = models.FileField(upload_to="videos",blank="True",null="True")
    likes = models.ManyToManyField(User,related_name="liked_posts",blank=True)


    class Meta:
        verbose_name_plural = "TravelPost"

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class TravelImage(models.Model):
    post = models.ForeignKey(TravelPost,on_delete=models.CASCADE,related_name='images')
    images = models.ImageField(upload_to="photos")

    def delete(self, *args, **kwargs):
        if self.images and os.path.isfile(self.images.path):
            os.remove(self.images.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Image for Post: {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(TravelPost,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic = models.ImageField(upload_to='profile_pic/',null=True,blank=True,default='profile_pic/user_profile.png')

    def __str__(self):
        return self.user.username

    @property
    def get_profile_pic_url(self):
        if self.profile_pic:
            return self.profile_pic.url
        return '/media/profile_pic/user_profile.png'


class Contact(models.Model):
    fullname = models.CharField(max_length=200,default="Unknown")
    email = models.EmailField()
    mobile = models.BigIntegerField()
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contact"

    def __str__(self):
        return self.fullname

