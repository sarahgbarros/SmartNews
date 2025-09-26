from django.contrib import admin
from .models import News, NewsCategory

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('category', 'published_date')

class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    


admin.site.register(News)
admin.site.register(NewsCategory)
