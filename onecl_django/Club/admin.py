from django.contrib import admin
from .models import (Category, Dept, Club)

# Register your models here.

admin.site.register(Category)
admin.site.register(Dept)
admin.site.register(Club)