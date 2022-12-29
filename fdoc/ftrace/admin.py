from django.contrib import admin
from .models import *
# Register your models here.

# from django.contrib import messages
# from django.utils.translation import ngettext

# class ZgerAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,                                             {'fields': ['zger_name']}),
#         (None,                                             {'fields': ['office']}),
#         (None,                                             {'fields': ['zger_sort']}),
#         (None,                                             {'fields': ['force_show']}),
#         (None,                                             {'fields': ['kicked']}),
       
#     ]
#     list_display = ('zger_name', 'office','kicked')
#     search_fields = ['zger_name','kicked']
#     list_filter = ['office','kicked',]
#     inlines = (QuoteRecordInline,)
#     actions = ['make_unkicked','make_kicked'] 
#     def make_unkicked(self, request, queryset):
#         updated = queryset.update(kicked=False)
#         self.message_user(request, ngettext(
#             '%d zger was successfully marked as unkicked.',
#             '%d zgers were successfully marked as unkicked.',
#             updated,) % updated, messages.SUCCESS)
#     def make_kicked(self, request, queryset):
#         updated = queryset.update(kicked=True)
#         self.message_user(request, ngettext(
#             '%d zger was successfully marked as kicked.',
#             '%d zgers were successfully marked as kicked.',
#             updated,) % updated, messages.SUCCESS)
# admin.site.register(Zger, ZgerAdmin)




# class QuoteAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,                                             {'fields': ['quote_name']}),
#         (None,                                             {'fields': ['quote_sort']}),
#         (None,                                             {'fields': ['force_show']}),
#         (None,                                             {'fields': ['quote_string']}),
#     ]
#     list_display = ('quote_name', 'quote_sort')
#     search_fields = ['quote_name']
#     inlines = (QuoteRecordInline,)
# admin.site.register(Quote, QuoteAdmin)