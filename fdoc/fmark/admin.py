from django.contrib import admin
from .models import Fmark

class FmarkAdmin(admin.ModelAdmin):
    list_display = ['subject', 'body']

admin.site.register(Fmark, FmarkAdmin)