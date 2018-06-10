from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from article.models import *

# Register your models here.
admin.site.register(Article)
admin.site.register(BaseProfile)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Labels)
admin.site.register(ProfileFollowers)
admin.site.register(ArticleLiked)
admin.site.register(User)


class ProfileInline(admin.StackedInline):
    model = BaseProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)