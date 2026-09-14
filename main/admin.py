from django.contrib import admin

from main.models import Experience, Project


admin.site.register(Experience)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "role", "display_order")
    ordering = ("display_order", "title")