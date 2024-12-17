from django.contrib import admin
from .models import Province, District, Sector, Cell, Tap, Village, ContactMessage, warsUser, Location, Password,userProfile,Case

# Register your models here.


@admin.register(warsUser)
class warsUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'names', 'email', 'phone', 'nationalId', 'dob','gender','nationality','emergencyContact','profile_pic', 'is_active', 'created_at', 'updated_at')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'country', 'province', 'district', 'sector', 'cell', 'village')

@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'password_hash', 'otp', 'otp_expiration_time', 'reset_token', 'reset_token_expiration', 'last_changed_at')

@admin.register(userProfile)
class userProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
@admin.register(Tap)
class TapAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'location','tap_id')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('title', 'user__username')
    actions = ['mark_resolved', 'mark_in_progress']

    # Add custom actions for bulk status changes
    @admin.action(description='Mark selected cases as Resolved')
    def mark_resolved(self, request, queryset):
        queryset.update(status='Resolved')

    @admin.action(description='Mark selected cases as In Progress')
    def mark_in_progress(self, request, queryset):
        queryset.update(status='In Progress')   


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province')

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district')

@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sector')

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cell')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'names', 'phone', 'email', 'message','file' ,'submitted_at')