from django.contrib import admin
from .models import Conditions, UserProfile, ConditionsText
import openpyxl
from django.http import HttpResponse
from django.contrib import admin
import requests


def export_users_to_excel(modeladmin, request, queryset):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Users'

    sheet.append(['Telegram ID', 'Username', 'Name'])

    for user in queryset:
        sheet.append([user.telegram_id, user.username, user.name])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    workbook.save(response)
    return response

export_users_to_excel.short_description = "Експортувати в Excel"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'name')
    actions = [export_users_to_excel]



admin.site.register(Conditions)
admin.site.register(ConditionsText)
