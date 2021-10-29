import unittest
import os

from src.consts import *
from src.Scanner import Scanner


class ScannerTestCase(unittest.TestCase):
    """This class represents the scanner test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        pass

    def tearDown(self):
        """Executed after tests"""

        pass

    def test_thread_count(self):
        """Tests scanner thread_count against google.com's ip address"""

        scanner = Scanner("172.253.124.102")

        self.assertEqual(scanner.max_threads, 1)

    def test_single_ip_address(self):
        """Tests scanner with single ip address from google.com"""
        stream = os.popen('scanner -t 172.253.124.102')
        output = stream.read()

        self.assertNotIn("Input Error", output)

        self.assertIn("172.253.124.102", output)

    def test_multiple_ips_addresses(self):
        """Tests scanner with multiple ip addresses from google.com and yahoo.com"""
        stream = os.popen('scanner -t "172.253.124.102,98.137.11.164"')
        output = stream.read()

        self.assertNotIn("Input Error", output)

        self.assertIn("172.253.124.102", output)

        self.assertIn("98.137.11.164", output)

    def test_malformed_input(self):
        """Tests scanner with malformed ip address"""
        stream = os.popen('scanner -t "=172.253.124.102"')
        output = stream.read()

        self.assertIn("Input Error", output)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
