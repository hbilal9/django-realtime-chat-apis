from django.contrib import admin
from .models import Thread, Message

# Register your models here.

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('first_person', 'second_person', 'created_at', 'updated_at')
    search_fields = ('first_person__username', 'second_person__username')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('thread', 'sender', 'text', 'created_at', 'updated_at')
    search_fields = ('thread__first_person__username', 'thread__second_person__username', 'sender__username')

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
