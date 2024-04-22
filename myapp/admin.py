from django.contrib import admin
from .models import PublicUser, UserAPIKey
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PublicUser)
admin.site.register(UserAPIKey)
