from django.contrib import admin, sites
from .models import Post, Category, Comment, Author, MyModel

from modeltranslation.admin import TranslationAdmin

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Author)


class CategoryAdmin(TranslationAdmin):
    model = Category


class MyModelAdmin(TranslationAdmin):
    model = MyModel


admin.site.register(MyModel)
admin.site.register(Category)

# Register your models here.
