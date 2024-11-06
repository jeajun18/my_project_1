from django.contrib import admin

from .models import Quote, Category

# Register your models here.

# 관리자 페이지에서 관리할 수 있도록 설정
admin.site.register(Quote)
admin.site.register(Category)


