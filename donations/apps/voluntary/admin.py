from django.contrib import admin
from donations.apps.voluntary.models import Address, Shelter, Voluntary, VoluntaryAllocation

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "cep", "city")
    search_fields = ("cep", "street", "city", "neighborhood")
    readonly_fields = ("id", "created_at", "updated_at",)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    readonly_fields = ("id", "created_at", "updated_at",)

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Voluntary)
class VoluntaryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "team_type", "phone")
    search_fields = ("name", "team_type")
    list_filter = ("team_type",)
    readonly_fields = ("id", "created_at", "updated_at", "cpf")

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(VoluntaryAllocation)
class VoluntaryAllocationAdmin(admin.ModelAdmin):
    list_display = ("id", "voluntary", "shelter")
    search_fields = ("voluntary__name", "shelter__name")
    list_filter = ("shelter__name",)