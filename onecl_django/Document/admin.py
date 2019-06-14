from django.contrib import admin
from .models import DocumentType, Document

# Register your models here.
admin.site.register(Document)
admin.site.register(DocumentType)