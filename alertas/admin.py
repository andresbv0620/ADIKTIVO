from django.contrib import admin
from .models import Alert, Match
# Register your models here.

class AlertAdmin(admin.ModelAdmin):
    list_display = ('user','main_category','brand','model','year_min','year_max','price_min','price_max','location','mileage')
    list_filter = ('user',)
    search_fields = ['user', 'main_category']
    #filter_horizontal = ('colector', 'formulario', 'tablets')

class MatchAdmin(admin.ModelAdmin):
    list_display = ("external_id" ,"title" ,"category_id" ,"price" ,"start_time","stop_time" ,"permalink" ,"thumbnail")
    list_filter = ('alerts',)
    #filter_horizontal = ('colector', 'formulario', 'tablets')

admin.site.register(Alert, AlertAdmin)
admin.site.register(Match, MatchAdmin)