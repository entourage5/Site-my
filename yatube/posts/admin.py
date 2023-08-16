from django.contrib import admin
from posts.models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ['text', 'pub_date', 'author', 'group']
    search_fields = ['text',]
    list_filter = ['pub_date',]
    # Это свойство сработает для всех колонок: где пусто — там будет эта строка
    empty_value_display = '-пусто-'
    list_editable = ['group',]


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
