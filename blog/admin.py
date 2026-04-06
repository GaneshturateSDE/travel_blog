from django.contrib import admin
from .models import TravelPost,TravelImage,Comment,Contact
# Register your models here.

admin.site.register(TravelPost)
admin.site.register(TravelImage)
admin.site.register(Comment)
admin.site.register(Contact)