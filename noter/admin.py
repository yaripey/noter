from django.contrib import admin

from .models import Notebook, Note


class NoteInline(admin.StackedInline):
    model = Note
    extra = 0

class NotebookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'user', 'desc']}),
    ]
    inlines = [NoteInline]


admin.site.register(Notebook, NotebookAdmin)

