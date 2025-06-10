#!/usr/bin/env python
"""
Test runner script for the Simple Note Taking App

This script provides convenient ways to run different test suites:
- Unit tests only
- Integration tests only  
- All tests
- Specific test classes or methods
- Tests with coverage reporting

Usage:
    python run_tests.py --unit                     # Run only unit tests
    python run_tests.py --integration             # Run only integration tests  
    python run_tests.py --all                     # Run all tests
    python run_tests.py --coverage               # Run all tests with coverage
    python run_tests.py --app notes_app          # Run tests for specific app
    python run_tests.py --class NoteModelTest    # Run specific test class
    python run_tests.py --verbose                # Run with verbose output
"""

import os
import sys
import subprocess
import argparse

# Add the project directory to Python path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notely_project.settings')

import django
django.setup()

from django.test.utils import get_runner
from django.conf import settings


def run_tests(test_labels, verbosity=1, interactive=False, keepdb=False, **kwargs):
    """Run Django tests with specified labels"""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=interactive,
        keepdb=keepdb,
        **kwargs
    )
    failures = test_runner.run_tests(test_labels)
    return failures


def run_with_coverage(test_labels, verbosity=1):
    """Run tests with coverage reporting"""
    try:
        import coverage
    except ImportError:
        print("Coverage.py not installed. Install with: pip install coverage")
        return 1
    
    # Start coverage
    cov = coverage.Coverage(source=['.'])
    cov.start()
    
    # Run tests
    failures = run_tests(test_labels, verbosity=verbosity)
    
    # Stop coverage and report
    cov.stop()
    cov.save()
    
    print("\n" + "="*50)
    print("COVERAGE REPORT")
    print("="*50)
    cov.report()
    
    # Generate HTML report
    html_dir = os.path.join(PROJECT_DIR, 'htmlcov')
    cov.html_report(directory=html_dir)
    print(f"\nHTML coverage report generated in: {html_dir}")
    
    return failures


def get_test_labels(args):
    """Generate test labels based on command line arguments"""
    labels = []
    
    if args.unit:
        # Unit test labels - tests that don't require API calls
        labels.extend([
            'notes_app.tests.test_models',
            'notes_app.tests.test_serializers', 
            'notes_app.tests.test_permissions',
            'users.tests.test_models',  # Add when created
            'users.tests.test_serializers',  # Add when created
        ])
    
    if args.integration:
        # Integration test labels - tests that test full API endpoints
        labels.extend([
            'notes_app.tests.test_api_integration',
            'notes_app.tests.test_admin_integration',
        ])
    
    if args.all or (not args.unit and not args.integration and not args.app and not args.class_name):
        # Run all tests if no specific option is given
        labels = ['notes_app.tests', 'users.tests']
    
    if args.app:
        labels = [f'{args.app}.tests']
    
    if args.class_name:
        # Find the test class in available apps
        for app in ['notes_app', 'users']:
            for test_file in ['test_models', 'test_serializers', 'test_permissions', 
                            'test_api_integration', 'test_admin_integration']:
                labels.append(f'{app}.tests.{test_file}.{args.class_name}')
    
    return labels


def main():
    parser = argparse.ArgumentParser(description='Run tests for Simple Note Taking App')
    
    # Test selection options
    parser.add_argument('--unit', action='store_true', 
                       help='Run only unit tests (models, serializers, permissions)')
    parser.add_argument('--integration', action='store_true',
                       help='Run only integration tests (API endpoints)')
    parser.add_argument('--all', action='store_true',
                       help='Run all tests')
    parser.add_argument('--app', type=str,
                       help='Run tests for specific app (e.g., notes_app)')
    parser.add_argument('--class', dest='class_name', type=str,
                       help='Run specific test class (e.g., NoteModelTest)')
    
    # Test execution options
    parser.add_argument('--coverage', action='store_true',
                       help='Run tests with coverage reporting')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Run tests with verbose output')
    parser.add_argument('--keepdb', action='store_true',
                       help='Keep test database between runs')
    parser.add_argument('--parallel', type=int,
                       help='Run tests in parallel (specify number of processes)')
    parser.add_argument('--failfast', action='store_true',
                       help='Stop on first test failure')
    
    args = parser.parse_args()
    
    # Set verbosity
    verbosity = 2 if args.verbose else 1
    
    # Get test labels
    test_labels = get_test_labels(args)
    
    print("Simple Note Taking App - Test Runner")
    print("="*40)
    print(f"Running tests: {', '.join(test_labels) if test_labels else 'All tests'}")
    print("="*40)
    
    # Prepare kwargs for test runner
    runner_kwargs = {}
    if args.parallel:
        runner_kwargs['parallel'] = args.parallel
    if args.failfast:
        runner_kwargs['failfast'] = True
    
    # Run tests
    if args.coverage:
        failures = run_with_coverage(test_labels, verbosity=verbosity)
    else:
        failures = run_tests(
            test_labels, 
            verbosity=verbosity, 
            keepdb=args.keepdb,
            **runner_kwargs
        )
    
    # Exit with appropriate code
    if failures:
        print(f"\n{failures} test(s) failed.")
        sys.exit(1)
    else:
        print("\nAll tests passed!")
        sys.exit(0)


if __name__ == '__main__':
    main() 