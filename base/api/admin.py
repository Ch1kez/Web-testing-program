from django.contrib import admin

from .models import Mail, Target, Test, Tuser, WebsiteTable


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    search_fields = ['tmail']  # Поля для поиска
    ordering = ['tmail']  # Поле для сортировки


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    search_fields = ['rem', 'tname']  # Поля для поиска
    list_filter = ['rem', 'tname']  # Поля для фильтрации
    ordering = ['rem', 'tname']  # Поле для сортировки


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    search_fields = ['id', 'test_name', 'test_grp']  # Поля для поиска
    list_filter = ['id', 'test_name', 'test_grp']  # Поля для фильтрации
    ordering = ['id', 'test_name', 'test_grp']  # Поле для сортировки


@admin.register(Tuser)
class TuserAdmin(admin.ModelAdmin):
    search_fields = ['target', 'ulogin', 'uorg']  # Поля для поиска
    list_filter = ['target', 'ulogin', 'uorg']  # Поля для фильтрации
    ordering = ['target', 'ulogin', 'uorg']  # Поле для сортировки


@admin.register(WebsiteTable)
class WebsiteTableAdmin(admin.ModelAdmin):
    search_fields = ['url']  # Поля для поиска
    ordering = ['url']  # Поле для сортировки
    # list_filter = ['custom_field']  # Пример поля для фильтрации
