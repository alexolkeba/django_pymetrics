from django.contrib import admin
from .models import (
    TraitDimension, TraitDefinition, TraitMeasurement, 
    TraitProfile, TraitMappingConfiguration
)


@admin.register(TraitDimension)
class TraitDimensionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['name', 'created_at']
    search_fields = ['name', 'description', 'scientific_basis']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Scientific Information', {
            'fields': ('scientific_basis',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TraitDefinition)
class TraitDefinitionAdmin(admin.ModelAdmin):
    list_display = ['name', 'dimension', 'reliability_coefficient', 'is_active', 'created_at']
    list_filter = ['dimension', 'is_active', 'normalization_method', 'created_at']
    search_fields = ['name', 'description', 'scientific_basis']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'dimension', 'description', 'is_active')
        }),
        ('Scientific Information', {
            'fields': ('scientific_basis', 'measurement_method', 'reliability_coefficient', 'validity_evidence')
        }),
        ('Configuration', {
            'fields': ('source_games', 'metrics_used', 'normalization_method', 'confidence_threshold')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TraitMeasurement)
class TraitMeasurementAdmin(admin.ModelAdmin):
    list_display = ['user', 'trait_definition', 'normalized_score', 'reliability_coefficient', 'calculation_timestamp']
    list_filter = ['trait_definition__dimension', 'game_type', 'calculation_timestamp']
    search_fields = ['user__username', 'trait_definition__name', 'session_id']
    readonly_fields = ['id', 'calculation_timestamp']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'trait_definition', 'session_id', 'game_type')
        }),
        ('Measurement Values', {
            'fields': ('raw_score', 'normalized_score', 'confidence_interval')
        }),
        ('Scientific Validation', {
            'fields': ('reliability_coefficient', 'validity_evidence')
        }),
        ('Metadata', {
            'fields': ('measurement_method', 'data_points_used', 'calculation_timestamp')
        }),
    )


@admin.register(TraitProfile)
class TraitProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'overall_confidence', 'data_completeness', 'traits_measured', 'created_at']
    list_filter = ['overall_confidence', 'data_completeness', 'created_at']
    search_fields = ['user__username', 'session_id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'session_id')
        }),
        ('Profile Data', {
            'fields': ('trait_scores', 'dimension_scores', 'confidence_scores')
        }),
        ('Quality Metrics', {
            'fields': ('overall_confidence', 'data_completeness', 'quality_score')
        }),
        ('Metadata', {
            'fields': ('calculation_method', 'traits_measured', 'total_data_points', 'created_at', 'updated_at')
        }),
    )


@admin.register(TraitMappingConfiguration)
class TraitMappingConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'version', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'version', 'is_active')
        }),
        ('Configuration Data', {
            'fields': ('trait_weights', 'normalization_settings', 'confidence_thresholds')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    ) 