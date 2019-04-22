from django.contrib import admin
from .models import User, GithubUserInfo


admin.site.register(User)
admin.site.register(GithubUserInfo)
