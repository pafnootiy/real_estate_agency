from django.contrib import admin
from .models import Flat, Complaint, Owner

class OwnerAdminInLine(admin.TabularInline):
    model = Owner.apartments.through
    raw_id_fields = ('owner',)

@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    inlines = [OwnerAdminInLine]
    search_fields = ("town", "address",)
    readonly_fields = ("created_at",)
    list_display = (
        "address", "price", "new_building", "construction_year", "town",  )
    list_editable = ("new_building",)
    raw_id_fields = ("likes",)
    list_filter = ("new_building", "has_balcony", "rooms_number")

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = (
        "owner", "phonenumber", "pure_phonenumber")
    raw_id_fields = ("apartments",)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ("person", "flat_trouble",)