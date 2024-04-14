import unittest
from unittest import defaultTestLoader

# Test files
import deck_test

def create_test_suite():
	suite = unittest.TestSuite()
	suite.addTests(defaultTestLoader.loadTestsFromModule(deck_test))
	return suite

if __name__ == '__main__':
	test_suite = create_test_suite()
	runner = unittest.TextTestRunner()
	result = runner.run(test_suite)