from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_summary', 'created_at')

    def content_summary(self, obj):
        # Определите, как вы хотите отображать краткое содержание контента
        return obj.content[:50]  # Например, отображаем первые 50 символов
    content_summary.short_description = 'Content'

admin.site.register(News, NewsAdmin)
