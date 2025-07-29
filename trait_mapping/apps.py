from django.apps import AppConfig


class TraitMappingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trait_mapping'
    verbose_name = 'Trait Mapping System'
    
    def ready(self):
        """Initialize the trait mapping system when the app is ready."""
        try:
            # Import and initialize the comprehensive trait system
            from .comprehensive_traits import ComprehensiveTraitSystem
            # This will be initialized when needed
        except ImportError:
            pass 