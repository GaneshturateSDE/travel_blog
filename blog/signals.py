from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# for delete image path
import os
from django.db.models.signals import pre_delete
from .models import TravelPost,TravelImage

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_delete,sender=TravelPost)
def delete_post_images(sender,instance,**kwargs):
    for image in instance.images.all():
        if image.images and os.path.isfile(image.images.path):
            os.remove(image.images.path) #delete the image file