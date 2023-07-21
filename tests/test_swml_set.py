import unittest
from swml import SWMLResponse, Set

class TestSWMLSet(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_set_method(self):
        main_section = self.response.add_section('main')
        main_section.set(variables={"var1": "value1", "var2": "value2"})
        expected_swml = '{"sections": {"main": [{"set": {"variables": {"var1": "value1", "var2": "value2"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_set_instance(self):
        main_section = self.response.add_section('main')
        set_instruction = Set(variables={"var1": "value1", "var2": "value2"})
        main_section.add_instruction(set_instruction)
        expected_swml = '{"sections": {"main": [{"set": {"variables": {"var1": "value1", "var2": "value2"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
