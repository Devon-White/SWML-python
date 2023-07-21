import unittest
from swml import SWMLResponse, Goto

class TestSWMLGoto(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_goto_method(self):
        main_section = self.response.add_section('main')
        main_section.goto(label="label1", when="var1 == 'value1'", max_=3, meta={"key": "value"})
        expected_swml = '{"sections": {"main": [{"goto": {"label": "label1", "when": "var1 == \'value1\'", "max": 3, "meta": {"key": "value"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_goto_instance(self):
        main_section = self.response.add_section('main')
        goto_instruction = Goto(label="label1", when="var1 == 'value1'", max_=3, meta={"key": "value"})
        main_section.add_instruction(goto_instruction)
        expected_swml = '{"sections": {"main": [{"goto": {"label": "label1", "when": "var1 == \'value1\'", "max": 3, "meta": {"key": "value"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)