# safety/admin.py

from django.contrib import admin
from .models import Equipment, ChecklistItem, CheckLog
from import_export.admin import ImportExportModelAdmin


@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'category')

@admin.register(ChecklistItem)
class ChecklistItemAdmin(ImportExportModelAdmin):
    list_display = ('id', 'question', 'category', 'order')

admin.site.register(CheckLog)