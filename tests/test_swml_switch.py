import unittest
from swml import SWMLResponse, Switch

class TestSWMLSwitch(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_switch_method(self):
        main_section = self.response.add_section('main')
        main_section.switch(variable="prompt_value", case={"1": ["goto: sales"], "2": ["play: https://example.com/hello.wav"]}, default=["play: https://example.com/no_match.wav"])
        expected_swml = '{"sections": {"main": [{"switch": {"variable": "prompt_value", "case": {"1": ["goto: sales"], "2": ["play: https://example.com/hello.wav"]}, "default": ["play: https://example.com/no_match.wav"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_switch_instance(self):
        main_section = self.response.add_section('main')
        switch_instruction = Switch(variable="prompt_value", case={"1": ["goto: sales"], "2": ["play: https://example.com/hello.wav"]}, default=["play: https://example.com/no_match.wav"])
        main_section.add_instruction(switch_instruction)
        expected_swml = '{"sections": {"main": [{"switch": {"variable": "prompt_value", "case": {"1": ["goto: sales"], "2": ["play: https://example.com/hello.wav"]}, "default": ["play: https://example.com/no_match.wav"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)