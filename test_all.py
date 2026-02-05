#!/usr/bin/env python
"""
Simple test runner for Drone Mission Framework
"""

import sys
import os

# Додаємо поточну директорію до Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def run_tests():
    """Run all tests"""
    import unittest
    
    print("=" * 70)
    print("DRONE MISSION FRAMEWORK - TEST SUITE")
    print("=" * 70)
    
    # Створюємо порожні __init__.py файли якщо їх немає
    test_dirs = [
        os.path.join(current_dir, 'tests'),
        os.path.join(current_dir, 'tests', 'unit'),
        os.path.join(current_dir, 'tests', 'integration')
    ]
    
    for test_dir in test_dirs:
        if not os.path.exists(test_dir):
            print(f"Creating directory: {test_dir}")
            os.makedirs(test_dir, exist_ok=True)
        
        init_file = os.path.join(test_dir, '__init__.py')
        if not os.path.exists(init_file):
            print(f"Creating: {init_file}")
            with open(init_file, 'w') as f:
                f.write('# Test package\n')
    
    # Завантажуємо тести вручну
    test_cases = []
    
    # Unit tests
    unit_tests = [
        'tests.unit.test_bridge',
        'tests.unit.test_template', 
        'tests.unit.test_strategy',
        'tests.unit.test_cor',
        'tests.unit.test_environment',
        'tests.unit.test_factory'
    ]
    
    # Integration tests
    integration_tests = [
        'tests.integration.test_mission_end_to_end'
    ]
    
    all_tests = unit_tests + integration_tests
    
    # Завантажуємо кожен тест
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_module in all_tests:
        try:
            module_suite = loader.loadTestsFromName(test_module)
            suite.addTest(module_suite)
            print(f"✓ Loaded: {test_module}")
        except Exception as e:
            print(f"✗ Failed to load {test_module}: {e}")
    
    if suite.countTestCases() == 0:
        print("\n❌ No tests loaded!")
        return 1
    
    print(f"\nTotal test cases: {suite.countTestCases()}")
    print("-" * 70)
    
    # Запускаємо тести
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ All tests PASSED!")
        return 0
    else:
        print("\n❌ Some tests FAILED!")
        return 1

def run_specific_test(test_name):
    """Run a specific test"""
    import unittest
    
    print(f"\nRunning specific test: {test_name}")
    print("=" * 50)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1

def list_tests():
    """List all available tests"""
    print("Available test modules:")
    print("-" * 30)
    
    test_modules = [
        ("Unit Tests:", [
            "tests.unit.test_bridge - Bridge pattern tests",
            "tests.unit.test_template - Template method tests", 
            "tests.unit.test_strategy - Strategy pattern tests",
            "tests.unit.test_cor - Chain of Responsibility tests",
            "tests.unit.test_environment - Environment tests",
            "tests.unit.test_factory - Factory pattern tests"
        ]),
        ("Integration Tests:", [
            "tests.integration.test_mission_end_to_end - Full mission tests"
        ])
    ]
    
    for category, tests in test_modules:
        print(category)
        for test in tests:
            print(f"  {test}")
        print()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Drone Mission Framework Test Runner')
    parser.add_argument('--test', '-t', help='Run specific test module')
    parser.add_argument('--list', '-l', action='store_true', help='List all tests')
    parser.add_argument('--demo', '-d', action='store_true', help='Run demo after tests')
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
        sys.exit(0)
    
    if args.test:
        # Запускаємо конкретний тест
        exit_code = run_specific_test(args.test)
    else:
        # Запускаємо всі тести
        exit_code = run_tests()
    
    # Запускаємо демо якщо треба
    if exit_code == 0 and args.demo:
        print("\n" + "=" * 70)
        print("RUNNING DEMO")
        print("=" * 70)
        try:
            from main import main
            main()
        except ImportError as e:
            print(f"Cannot run demo: {e}")
        except Exception as e:
            print(f"Demo error: {e}")
    
    sys.exit(exit_code)