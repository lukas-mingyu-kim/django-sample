from django.contrib import admin

from sample_api import models


admin.site.register(models.AtmUser)
admin.site.register(models.Account)
