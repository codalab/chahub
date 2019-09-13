from django.contrib import admin
from .models import User, GithubUserInfo, Profile, EmailAddress


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(EmailAddress)
admin.site.register(GithubUserInfo)
