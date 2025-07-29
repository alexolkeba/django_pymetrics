"""
Comprehensive tests for configuration management components.

Tests cover SettingsManager, ScientificConfig, and configuration validation
with various scenarios including edge cases and validation.
"""

import unittest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, override_settings

from config.settings_manager import SettingsManager
from config.scientific_config import ScientificConfig, TraitConfiguration, ScientificParameter


class TestSettingsManager(TestCase):
    """Test cases for SettingsManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary config file
        self.temp_config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_config_path = self.temp_config_file.name
        
        # Initial test configuration
        self.test_config = {
            'behavioral_data': {
                'data_retention_days': 365,
                'min_session_duration_ms': 30000,
                'event_batch_size': 100
            },
            'scientific_validation': {
                'min_data_completeness': 80.0,
                'min_quality_score': 70.0,
                'confidence_interval_level': 0.95
            },
            'agents': {
                'event_logger': {
                    'enabled': True,
                    'batch_size': 50
                }
            }
        }
        
        # Write test config to file
        json.dump(self.test_config, self.temp_config_file, indent=2)
        self.temp_config_file.close()
        
        # Initialize settings manager with test config
        self.settings_manager = SettingsManager(self.temp_config_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary config file
        if os.path.exists(self.temp_config_path):
            os.unlink(self.temp_config_path)
    
    def test_load_configuration_from_file(self):
        """Test loading configuration from file."""
        # Verify configuration was loaded
        self.assertEqual(
            self.settings_manager.get('behavioral_data.data_retention_days'),
            180  # This is set in the test configuration
        )
        self.assertEqual(
            self.settings_manager.get('scientific_validation.min_data_completeness'),
            80.0
        )
    
    def test_get_nested_configuration_values(self):
        """Test getting nested configuration values using dot notation."""
        # Test existing values
        self.assertEqual(
            self.settings_manager.get('behavioral_data.min_session_duration_ms'),
            30000
        )
        self.assertEqual(
            self.settings_manager.get('agents.event_logger.enabled'),
            True
        )
        
        # Test non-existent values with defaults
        self.assertEqual(
            self.settings_manager.get('nonexistent.key', 'default_value'),
            'default_value'
        )
        self.assertIsNone(
            self.settings_manager.get('nonexistent.key')
        )
    
    def test_set_configuration_values(self):
        """Test setting configuration values."""
        # Set new value
        self.settings_manager.set('test.new_key', 'test_value')
        self.assertEqual(
            self.settings_manager.get('test.new_key'),
            'test_value'
        )
        
        # Update existing value
        self.settings_manager.set('behavioral_data.data_retention_days', 180)
        self.assertEqual(
            self.settings_manager.get('behavioral_data.data_retention_days'),
            180
        )
        
        # Set nested value
        self.settings_manager.set('new.nested.deep.value', 42)
        self.assertEqual(
            self.settings_manager.get('new.nested.deep.value'),
            42
        )
    
    def test_save_and_reload_configuration(self):
        """Test saving configuration to file and reloading."""
        # Modify configuration
        self.settings_manager.set('test.save_key', 'save_value')
        
        # Save to file
        self.settings_manager.save_configuration()
        
        # Create new settings manager instance
        new_settings_manager = SettingsManager(self.temp_config_path)
        
        # Verify value was persisted
        self.assertEqual(
            new_settings_manager.get('test.save_key'),
            'save_value'
        )
    
    def test_validate_configuration(self):
        """Test configuration validation."""
        validation_result = self.settings_manager.validate_configuration()
        
        self.assertIn('valid', validation_result)
        self.assertIn('errors', validation_result)
        self.assertIn('warnings', validation_result)
        self.assertIn('sections_validated', validation_result)
        
        # Should be valid with test configuration
        self.assertTrue(validation_result['valid'])
    
    def test_validate_invalid_configuration(self):
        """Test validation with invalid configuration."""
        # Set invalid values
        self.settings_manager.set('behavioral_data.min_session_duration_ms', 100000)
        self.settings_manager.set('behavioral_data.max_session_duration_ms', 50000)  # Less than min
        
        validation_result = self.settings_manager.validate_configuration()
        
        self.assertFalse(validation_result['valid'])
        self.assertGreater(len(validation_result['errors']), 0)
    
    def test_get_section(self):
        """Test getting entire configuration sections."""
        behavioral_section = self.settings_manager.get_section('behavioral_data')
        
        self.assertIsInstance(behavioral_section, dict)
        self.assertIn('data_retention_days', behavioral_section)
        self.assertIn('min_session_duration_ms', behavioral_section)
    
    def test_update_section(self):
        """Test updating entire configuration sections."""
        new_section_data = {
            'new_setting_1': 'value1',
            'new_setting_2': 'value2'
        }
        
        self.settings_manager.update_section('new_section', new_section_data)
        
        retrieved_section = self.settings_manager.get_section('new_section')
        self.assertEqual(retrieved_section, new_section_data)
    
    def test_environment_specific_config(self):
        """Test environment-specific configuration."""
        # Test development environment
        self.settings_manager.set('deployment.environment', 'development')
        dev_config = self.settings_manager.get_environment_config()
        
        self.assertTrue(dev_config['debug'])
        self.assertEqual(dev_config['log_level'], 'DEBUG')
        
        # Test production environment
        self.settings_manager.set('deployment.environment', 'production')
        prod_config = self.settings_manager.get_environment_config()
        
        self.assertFalse(prod_config['debug'])
        self.assertEqual(prod_config['log_level'], 'WARNING')
    
    def test_export_import_configuration(self):
        """Test exporting and importing configuration."""
        # Create temporary export file
        export_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        export_path = export_file.name
        export_file.close()
        
        try:
            # Export configuration
            self.settings_manager.export_configuration(export_path)
            
            # Verify export file exists and has content
            self.assertTrue(os.path.exists(export_path))
            
            with open(export_path, 'r') as f:
                exported_config = json.load(f)
            
            self.assertIn('behavioral_data', exported_config)
            
            # Create new settings manager and import
            new_settings_manager = SettingsManager()
            new_settings_manager.import_configuration(export_path)
            
            # Verify imported values
            self.assertEqual(
                new_settings_manager.get('behavioral_data.data_retention_days'),
                365
            )
            
        finally:
            # Clean up export file
            if os.path.exists(export_path):
                os.unlink(export_path)
    
    def test_configuration_caching(self):
        """Test configuration value caching."""
        # First access should cache the value
        value1 = self.settings_manager.get('behavioral_data.data_retention_days')
        
        # Modify underlying config data directly (bypass cache)
        self.settings_manager.config_data['behavioral_data']['data_retention_days'] = 999
        
        # Second access should return cached value
        value2 = self.settings_manager.get('behavioral_data.data_retention_days')
        self.assertEqual(value1, value2)
        
        # Setting new value should clear cache
        self.settings_manager.set('behavioral_data.data_retention_days', 180)
        value3 = self.settings_manager.get('behavioral_data.data_retention_days')
        self.assertEqual(value3, 180)


class TestScientificConfig(TestCase):
    """Test cases for ScientificConfig class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scientific_config = ScientificConfig()
    
    def test_initialize_scientific_parameters(self):
        """Test initialization of scientific parameters."""
        # Check that key parameters are initialized
        bart_mean = self.scientific_config.get_parameter('bart_population_mean_pumps')
        self.assertIsNotNone(bart_mean)
        self.assertIsInstance(bart_mean, ScientificParameter)
        
        # Verify parameter properties
        self.assertEqual(bart_mean.name, "BART Population Mean Pumps")
        self.assertEqual(bart_mean.value, 30.5)
        self.assertGreater(len(bart_mean.validation_studies), 0)
    
    def test_parameter_validation(self):
        """Test scientific parameter validation."""
        bart_mean = self.scientific_config.get_parameter('bart_population_mean_pumps')
        
        # Test valid value
        self.assertTrue(bart_mean.validate())
        
        # Test invalid value (outside range)
        original_value = bart_mean.value
        bart_mean.value = 100.0  # Outside max_value
        self.assertFalse(bart_mean.validate())
        
        # Restore original value
        bart_mean.value = original_value
        self.assertTrue(bart_mean.validate())
    
    def test_set_parameter_with_validation(self):
        """Test setting parameters with validation."""
        # Test valid parameter update
        success = self.scientific_config.set_parameter('bart_population_mean_pumps', 35.0)
        self.assertTrue(success)
        
        updated_param = self.scientific_config.get_parameter('bart_population_mean_pumps')
        self.assertEqual(updated_param.value, 35.0)
        
        # Test invalid parameter update
        success = self.scientific_config.set_parameter('bart_population_mean_pumps', 100.0)
        self.assertFalse(success)
        
        # Value should remain unchanged
        param_after_invalid = self.scientific_config.get_parameter('bart_population_mean_pumps')
        self.assertEqual(param_after_invalid.value, 35.0)
    
    def test_trait_configurations(self):
        """Test trait configuration management."""
        # Test getting trait configuration
        risk_config = self.scientific_config.get_trait_config('risk_tolerance')
        self.assertIsNotNone(risk_config)
        self.assertIsInstance(risk_config, TraitConfiguration)
        
        # Verify configuration properties
        self.assertEqual(risk_config.trait_name, 'risk_tolerance')
        self.assertTrue(risk_config.enabled)
        self.assertGreater(risk_config.confidence_threshold, 0.0)
        self.assertGreater(len(risk_config.source_metrics), 0)
    
    def test_trait_configuration_validation(self):
        """Test trait configuration validation."""
        # Create valid configuration
        valid_config = TraitConfiguration(
            trait_name='test_trait',
            confidence_threshold=0.75,
            min_sample_size=10,
            source_metrics=['metric1', 'metric2'],
            reliability_coefficient=0.80
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Create invalid configuration
        invalid_config = TraitConfiguration(
            trait_name='invalid_trait',
            confidence_threshold=1.5,  # Invalid: > 1.0
            min_sample_size=-5,        # Invalid: < 1
            source_metrics=[],         # Invalid: empty
            reliability_coefficient=1.2  # Invalid: > 1.0
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
    
    def test_update_trait_configuration(self):
        """Test updating trait configurations."""
        # Create new configuration
        new_config = TraitConfiguration(
            trait_name='test_trait',
            confidence_threshold=0.8,
            min_sample_size=15,
            source_metrics=['test_metric1', 'test_metric2'],
            reliability_coefficient=0.85
        )
        
        # Update configuration
        success = self.scientific_config.update_trait_config('test_trait', new_config)
        self.assertTrue(success)
        
        # Verify update
        retrieved_config = self.scientific_config.get_trait_config('test_trait')
        self.assertEqual(retrieved_config.confidence_threshold, 0.8)
        self.assertEqual(retrieved_config.min_sample_size, 15)
    
    def test_validation_thresholds(self):
        """Test validation threshold management."""
        # Test getting validation thresholds
        min_completeness = self.scientific_config.get_validation_threshold('min_data_completeness')
        self.assertIsNotNone(min_completeness)
        self.assertEqual(min_completeness, 0.80)
        
        # Test non-existent threshold
        non_existent = self.scientific_config.get_validation_threshold('non_existent_threshold')
        self.assertIsNone(non_existent)
    
    def test_scientific_integrity_validation(self):
        """Test scientific integrity validation."""
        validation_result = self.scientific_config.validate_scientific_integrity()
        
        self.assertIn('valid', validation_result)
        self.assertIn('errors', validation_result)
        self.assertIn('warnings', validation_result)
        self.assertIn('recommendations', validation_result)
        
        # Should be valid with default configuration
        self.assertTrue(validation_result['valid'])
    
    def test_scientific_integrity_with_invalid_data(self):
        """Test scientific integrity validation with invalid data."""
        # Set invalid parameter value
        self.scientific_config.set_parameter('bart_population_mean_pumps', 100.0)  # Will fail
        
        # Create invalid trait configuration
        invalid_config = TraitConfiguration(
            trait_name='invalid_trait',
            confidence_threshold=1.5,  # Invalid
            source_metrics=[]  # Invalid
        )
        self.scientific_config.trait_configs['invalid_trait'] = invalid_config
        
        validation_result = self.scientific_config.validate_scientific_integrity()
        
        self.assertFalse(validation_result['valid'])
        self.assertGreater(len(validation_result['errors']), 0)
    
    def test_export_scientific_config(self):
        """Test exporting scientific configuration."""
        exported_config = self.scientific_config.export_scientific_config()
        
        self.assertIn('parameters', exported_config)
        self.assertIn('trait_configurations', exported_config)
        self.assertIn('validation_thresholds', exported_config)
        self.assertIn('research_metadata', exported_config)
        
        # Verify parameters are properly exported
        parameters = exported_config['parameters']
        self.assertIn('bart_population_mean_pumps', parameters)
        
        bart_param = parameters['bart_population_mean_pumps']
        self.assertIn('name', bart_param)
        self.assertIn('value', bart_param)
        self.assertIn('research_basis', bart_param)
    
    def test_research_citations(self):
        """Test research citation functionality."""
        # Test getting citation for existing trait
        citation = self.scientific_config.get_research_citation('risk_tolerance')
        self.assertIsNotNone(citation)
        self.assertIn('BART', citation)  # Should mention BART methodology
        
        # Test getting citation for non-existent trait
        no_citation = self.scientific_config.get_research_citation('non_existent_trait')
        self.assertIsNone(no_citation)
    
    def test_reliability_information(self):
        """Test reliability information retrieval."""
        # Test getting reliability info for existing trait
        reliability_info = self.scientific_config.get_reliability_info('risk_tolerance')
        self.assertIsNotNone(reliability_info)
        
        self.assertIn('reliability_coefficient', reliability_info)
        self.assertIn('validity_evidence', reliability_info)
        self.assertIn('scientific_basis', reliability_info)
        
        # Verify values are reasonable
        self.assertGreater(reliability_info['reliability_coefficient'], 0.0)
        self.assertLessEqual(reliability_info['reliability_coefficient'], 1.0)
        
        # Test getting reliability info for non-existent trait
        no_info = self.scientific_config.get_reliability_info('non_existent_trait')
        self.assertIsNone(no_info)


class TestConfigurationIntegration(TestCase):
    """Integration tests for configuration components."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_config_path = self.temp_config_file.name
        self.temp_config_file.close()
        
        self.settings_manager = SettingsManager(self.temp_config_path)
        self.scientific_config = ScientificConfig()
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        if os.path.exists(self.temp_config_path):
            os.unlink(self.temp_config_path)
    
    def test_settings_scientific_config_integration(self):
        """Test integration between settings manager and scientific config."""
        # Update settings with scientific parameters
        scientific_export = self.scientific_config.export_scientific_config()
        self.settings_manager.update_section('scientific_parameters', scientific_export)
        
        # Verify integration
        bart_param_from_settings = self.settings_manager.get(
            'scientific_parameters.parameters.bart_population_mean_pumps.value'
        )
        bart_param_from_scientific = self.scientific_config.get_parameter(
            'bart_population_mean_pumps'
        ).value
        
        self.assertEqual(bart_param_from_settings, bart_param_from_scientific)
    
    def test_configuration_persistence_workflow(self):
        """Test complete configuration persistence workflow."""
        # 1. Modify scientific configuration
        self.scientific_config.set_parameter('bart_population_mean_pumps', 32.0)
        
        # 2. Export to settings manager
        scientific_export = self.scientific_config.export_scientific_config()
        self.settings_manager.update_section('scientific', scientific_export)
        
        # 3. Save to file
        self.settings_manager.save_configuration()
        
        # 4. Create new instances and load from file
        new_settings_manager = SettingsManager(self.temp_config_path)
        
        # 5. Verify persistence
        loaded_value = new_settings_manager.get('scientific.parameters.bart_population_mean_pumps.value')
        self.assertEqual(loaded_value, 32.0)
    
    @override_settings(
        BEHAVIORAL_DATA_SETTINGS={'data_retention_days': 180},
        SCIENTIFIC_VALIDATION_SETTINGS={'min_data_completeness': 85.0}
    )
    def test_django_settings_integration(self):
        """Test integration with Django settings."""
        # Create new settings manager to pick up Django settings
        django_settings_manager = SettingsManager(self.temp_config_path)
        
        # Verify Django settings are merged
        retention_days = django_settings_manager.get('behavioral_data.data_retention_days')
        min_completeness = django_settings_manager.get('scientific_validation.min_data_completeness')
        
        self.assertEqual(retention_days, 180)
        self.assertEqual(min_completeness, 85.0)


if __name__ == '__main__':
    unittest.main()
