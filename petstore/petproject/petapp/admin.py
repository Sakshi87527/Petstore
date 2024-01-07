from django.contrib import admin
from . import models
# Register your models here.
#admin.site.register(models.pet)
class petadmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name","breed")}
admin.site.register(models.pet,petadmin) # petadmin automatically register 