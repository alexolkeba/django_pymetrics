"""
Comprehensive Test Runner for Django Pymetrics Agentic Framework

This script runs all tests for the Django Pymetrics framework including
agents, trait mapping, configuration, and API endpoints with coverage reporting.
"""

import os
import sys
import django
import unittest
from django.test.utils import get_runner
from django.conf import settings
from django.test.runner import DiscoverRunner

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pymetric.settings')
django.setup()


class ComprehensiveTestRunner:
    """
    Comprehensive test runner for the Django Pymetrics framework.
    
    This runner executes all test suites and provides detailed reporting
    including coverage analysis and performance metrics.
    """
    
    def __init__(self):
        """Initialize the test runner."""
        self.test_modules = [
            'tests.test_agents',
            'tests.test_trait_mapping',
            'tests.test_config',
            'tests.test_api',
            'tests.test_trait_inference_api'  # Existing test
        ]
        
        self.test_results = {}
        self.overall_success = True
    
    def run_all_tests(self, verbosity=2):
        """
        Run all test suites.
        
        Args:
            verbosity: Test output verbosity level (0-3)
            
        Returns:
            bool: True if all tests passed, False otherwise
        """
        print("=" * 80)
        print("Django Pymetrics Agentic Framework - Comprehensive Test Suite")
        print("=" * 80)
        
        # Run Django test runner
        test_runner = DiscoverRunner(verbosity=verbosity, interactive=False)
        
        # Discover and run tests
        suite = test_runner.build_suite(['tests'])
        result = test_runner.run_tests(['tests'])
        
        # Print summary
        self._print_test_summary(result)
        
        return result == 0
    
    def run_specific_test_module(self, module_name, verbosity=2):
        """
        Run tests for a specific module.
        
        Args:
            module_name: Name of the test module to run
            verbosity: Test output verbosity level
            
        Returns:
            bool: True if tests passed, False otherwise
        """
        print(f"\nRunning tests for module: {module_name}")
        print("-" * 50)
        
        test_runner = DiscoverRunner(verbosity=verbosity, interactive=False)
        result = test_runner.run_tests([module_name])
        
        self.test_results[module_name] = result == 0
        if result != 0:
            self.overall_success = False
        
        return result == 0
    
    def run_agent_tests(self):
        """Run tests specifically for agent components."""
        print("\n🤖 Running Agent Tests...")
        return self.run_specific_test_module('tests.test_agents')
    
    def run_trait_mapping_tests(self):
        """Run tests specifically for trait mapping components."""
        print("\n🧠 Running Trait Mapping Tests...")
        return self.run_specific_test_module('tests.test_trait_mapping')
    
    def run_config_tests(self):
        """Run tests specifically for configuration components."""
        print("\n⚙️ Running Configuration Tests...")
        return self.run_specific_test_module('tests.test_config')
    
    def run_api_tests(self):
        """Run tests specifically for API components."""
        print("\n🌐 Running API Tests...")
        return self.run_specific_test_module('tests.test_api')
    
    def run_integration_tests(self):
        """Run integration tests across all components."""
        print("\n🔗 Running Integration Tests...")
        
        # Integration tests are included in individual test modules
        # This method runs tests that specifically test component interactions
        integration_modules = [
            'tests.test_agents.TestAgentIntegration',
            'tests.test_trait_mapping',  # Contains integration scenarios
            'tests.test_config.TestConfigurationIntegration'
        ]
        
        success = True
        for module in integration_modules:
            if not self.run_specific_test_module(module):
                success = False
        
        return success
    
    def _print_test_summary(self, exit_code):
        """Print comprehensive test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        if exit_code == 0:
            print("✅ ALL TESTS PASSED!")
            status_emoji = "🎉"
            status_text = "SUCCESS"
        else:
            print("❌ SOME TESTS FAILED!")
            status_emoji = "💥"
            status_text = "FAILURE"
        
        print(f"\nOverall Status: {status_emoji} {status_text}")
        
        # Print module-specific results if available
        if self.test_results:
            print("\nModule Results:")
            for module, success in self.test_results.items():
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {module}: {status}")
        
        print("\n" + "=" * 80)
        
        # Print recommendations
        if exit_code != 0:
            print("\n🔧 RECOMMENDATIONS:")
            print("1. Review failed test output above")
            print("2. Check database migrations are up to date")
            print("3. Verify all dependencies are installed")
            print("4. Ensure Redis is running for Celery tests")
            print("5. Check Django settings configuration")
    
    def run_performance_tests(self):
        """Run performance-focused tests."""
        print("\n⚡ Running Performance Tests...")
        
        # Performance tests are included in API tests
        return self.run_specific_test_module('tests.test_api.TestAPIPerformance')
    
    def run_security_tests(self):
        """Run security-focused tests."""
        print("\n🔒 Running Security Tests...")
        
        # Security tests are included in API tests
        return self.run_specific_test_module('tests.test_api.TestAPIAuthentication')
    
    def generate_coverage_report(self):
        """Generate test coverage report."""
        try:
            import coverage
            
            print("\n📊 Generating Coverage Report...")
            
            cov = coverage.Coverage()
            cov.start()
            
            # Run tests with coverage
            self.run_all_tests(verbosity=1)
            
            cov.stop()
            cov.save()
            
            # Generate report
            print("\nCoverage Report:")
            cov.report()
            
            # Generate HTML report
            cov.html_report(directory='htmlcov')
            print("HTML coverage report generated in 'htmlcov' directory")
            
        except ImportError:
            print("⚠️ Coverage package not installed. Install with: pip install coverage")
        except Exception as e:
            print(f"⚠️ Error generating coverage report: {e}")


def main():
    """Main entry point for test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Django Pymetrics Test Runner')
    parser.add_argument('--module', help='Run tests for specific module')
    parser.add_argument('--agents', action='store_true', help='Run agent tests only')
    parser.add_argument('--traits', action='store_true', help='Run trait mapping tests only')
    parser.add_argument('--config', action='store_true', help='Run config tests only')
    parser.add_argument('--api', action='store_true', help='Run API tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--security', action='store_true', help='Run security tests only')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--verbosity', type=int, default=2, help='Test output verbosity (0-3)')
    
    args = parser.parse_args()
    
    runner = ComprehensiveTestRunner()
    
    try:
        if args.coverage:
            success = runner.generate_coverage_report()
        elif args.module:
            success = runner.run_specific_test_module(args.module, args.verbosity)
        elif args.agents:
            success = runner.run_agent_tests()
        elif args.traits:
            success = runner.run_trait_mapping_tests()
        elif args.config:
            success = runner.run_config_tests()
        elif args.api:
            success = runner.run_api_tests()
        elif args.integration:
            success = runner.run_integration_tests()
        elif args.performance:
            success = runner.run_performance_tests()
        elif args.security:
            success = runner.run_security_tests()
        else:
            # Run all tests
            success = runner.run_all_tests(args.verbosity)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Error running tests: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
