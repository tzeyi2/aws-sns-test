from django.contrib import admin
from django.forms.models import model_to_dict

from .forms import RegionConfigurationForm
from .models import (
    ExternalSourceEmissionFactor, UpdateExternalSourceEmissionFactor,
    PantasEmissionFactor, RegionConfiguration, RegionGeocode,
    ClimatiqVersion
)
from green.admin import LocalDatetimeMixin


@admin.register(ExternalSourceEmissionFactor)
class ExternalSourceEmissionFactorAdmin(admin.ModelAdmin):
    list_display = (
        'pantasemissionfactor', 'external_source_page_link',
        'external_source_id', 'name', 'description', 'source', 'source_link',
        'year_released', 'region', 'region_code', 'sector', 'category',
        'unit_type', 'lca_activity', 'method_applied', 'method_supported',
        'origin', 'unit', 'emission_factor_value', 'external_source_name',
        'created_at', 'updated_at')
    list_select_related = ('pantasemissionfactor',)
    readonly_fields = ('pantasemissionfactor',)
    search_fields = (
        'pantasemissionfactor__external_id', 'external_source_page_link', 'external_source_id', 'name',
        'description', 'source', 'source_link', 'year_released', 'region',
        'region_code', 'sector', 'category', 'unit_type', 'lca_activity',
        'method_applied', 'method_supported', 'origin', 'unit',
        'emission_factor_value', 'external_source_name', 'created_at',
        'updated_at')
    list_filter = ('unit_type', 'category', 'source')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UpdateExternalSourceEmissionFactor)
class UpdateExternalSourceEmissionFactorAdmin(admin.ModelAdmin):
    list_display = (
        'external_source_emission_factor', 'external_source_page_link',
        'external_source_id', 'name', 'description', 'source', 'source_link',
        'year_released', 'region', 'region_code', 'sector', 'category',
        'unit_type', 'lca_activity', 'method_applied', 'method_supported',
        'origin', 'unit', 'emission_factor_value', 'external_source_name',
        'remarks', 'created_at', 'updated_at')
    search_fields = (
        'external_source_emission_factor__id',
        'external_source_emission_factor__external_source_id',
        'name', 'description', 'source', 'year_released', 'region', 'sector',
        'category', 'unit_type')
    raw_id_fields = ("external_source_emission_factor",)

    autocomplete_fields = ('created_by',)

    def reset_original_data(self, obj):
        external_source__emission_factor_obj = obj.external_source_emission_factor
        pantas_emission_factor_obj = PantasEmissionFactor.objects.get(
            external_source_emission_factor=obj.external_source_emission_factor)

        for key, value in model_to_dict(external_source__emission_factor_obj).items():
            if key not in ['created_at', 'updated_at', 'external_source_page_link', 'external_source_id', 'raw_data']:
                setattr(pantas_emission_factor_obj, key, value)
        pantas_emission_factor_obj.save()

    # If BD add/update the record, means that the changes will reflect on PantasEmissionFactor
    def save_model(self, request, obj, form, change):
        obj.save()
        pantas_emission_factor_obj = PantasEmissionFactor.objects.get(
            external_source_emission_factor=obj.external_source_emission_factor)

        for key, value in model_to_dict(obj).items():
            if value and key not in ['id', 'external_source_emission_factor', 'remarks', 'created_by']:
                setattr(pantas_emission_factor_obj, key, value)
        pantas_emission_factor_obj.save()

    def delete_model(self, request, obj):
        self.reset_original_data(obj)
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.reset_original_data(obj)
        queryset.delete()


@admin.register(PantasEmissionFactor)
class PantasEmissionFactorAdmin(admin.ModelAdmin):
    list_display = (
        'external_id', 'external_source_emission_factor', 'name',
        'description', 'source', 'source_link', 'year_released', 'region',
        'region_code', 'sector', 'category', 'unit_type', 'lca_activity',
        'method_applied', 'method_supported', 'origin', 'unit',
        'emission_factor_value', 'external_source_name', 'created_at',
        'updated_at')
    readonly_fields = (
        'external_id', 'external_source_emission_factor', 'name',
        'description', 'source', 'source_link', 'year_released', 'region',
        'region_code', 'sector', 'category', 'unit_type', 'lca_activity',
        'method_applied', 'method_supported', 'origin', 'unit',
        'emission_factor_value', 'external_source_name', 'created_at',
        'updated_at')
    search_fields = (
        'external_id',
        'external_source_emission_factor__id',
        'external_source_emission_factor__external_source_id',
        'name', 'description', 'source', 'year_released', 'region', 'sector',
        'category', 'unit_type')
    list_filter = ('unit_type', 'category', 'source')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(RegionConfiguration)
class RegionConfigurationAdmin(LocalDatetimeMixin, admin.ModelAdmin):
    list_display = ('climatiq_region', 'blocklist', 'allowlist',
                    'created_at_local_date', 'created_at_local_time', 'remark')
    search_fields = ('climatiq_region', 'blocklist', 'allowlist')

    local_datetimes = ('created_at',)

    form = RegionConfigurationForm


@admin.register(RegionGeocode)
class RegionGeocodeAdmin(LocalDatetimeMixin, admin.ModelAdmin):
    list_display = ('region', 'country', 'latitude', 'longitude', 'created_at_local_date',
                    'created_at_local_time')
    search_fields = ('region',)

    local_datetimes = ('created_at',)


@admin.register(ClimatiqVersion)
class ClimatiqVersionAdmin(LocalDatetimeMixin, admin.ModelAdmin):
    list_display = ('latest', 'latest_minor', 'latest_major', 'updated_at')
    local_datetimes = ('updated_at',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
