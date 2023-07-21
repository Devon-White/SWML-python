import unittest
from swml import SWMLResponse, Request

class TestSWMLRequest(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_request_method(self):
        main_section = self.response.add_section('main')
        main_section.request(url="http://example.com", method="GET", headers={"Content-Type": "application/json"}, body={"key": "value"}, timeout=30.0, connect_timeout=5.0, save_variables=True)
        expected_swml = '{"sections": {"main": [{"request": {"url": "http://example.com", "method": "GET", "headers": {"Content-Type": "application/json"}, "body": {"key": "value"}, "timeout": 30.0, "connect_timeout": 5.0, "save_variables": true}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_request_instance(self):
        main_section = self.response.add_section('main')
        request_instruction = Request(url="http://example.com", method="GET", headers={"Content-Type": "application/json"}, body={"key": "value"}, timeout=30.0, connect_timeout=5.0, save_variables=True)
        main_section.add_instruction(request_instruction)
        expected_swml = '{"sections": {"main": [{"request": {"url": "http://example.com", "method": "GET", "headers": {"Content-Type": "application/json"}, "body": {"key": "value"}, "timeout": 30.0, "connect_timeout": 5.0, "save_variables": true}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

