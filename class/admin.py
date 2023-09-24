from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.student)
admin.site.register(models.teacher)
admin.site.register(models.Material)
admin.site.register(models.Class)
admin.site.register(models.Question)