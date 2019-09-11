from django.contrib import admin
from .models import User, GithubUserInfo, Profile


admin.site.register(User)
admin.site.register(GithubUserInfo)
admin.site.register(Profile)
