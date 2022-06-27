from django.contrib import admin
from .models import User
# Register your models here.
class UserRef(admin.ModelAdmin):
    list_display = ['id','first_name','username','email','address']
admin.site.register(User,UserRef)