from django.contrib import admin
from managehost import models
# Register your models here.

admin.site.register(models.HostInfo)
admin.site.register(models.HostType)
admin.site.register(models.UserInfo)