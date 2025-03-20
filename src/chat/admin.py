from django.utils.html import format_html
from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("country_with_flag", "chat_type", "user_package")

    def country_with_flag(self, obj):
        """
        Display the flag + country name in admin.
        """
        return format_html(f"{obj.country_flag} {obj.country_name}")

    country_with_flag.short_description = "Country"
