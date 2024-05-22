from django.contrib import admin

from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.LinkedEmail)
admin.site.register(models.Institution)
admin.site.register(models.InstitutionAccount)
