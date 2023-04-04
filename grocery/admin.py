from django.contrib import admin

from .models import Storage, Item, Ticket

class StorageAdmin(admin.ModelAdmin):
    fields = ["name", "users"]

admin.site.register(Storage, StorageAdmin)
admin.site.register(Item)
admin.site.register(Ticket)


# Register your models here.
