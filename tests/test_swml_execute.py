import unittest
from swml import SWMLResponse, Execute


class TestSWMLExecute(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_execute_method(self):
        main_section = self.response.add_section('main')
        main_section.execute(dest="section2", params={"param1": "value1"}, meta={"meta1": "value1"},
                             on_return={"return1": "value1"})
        expected_swml = '{"sections": {"main": [{"execute": {"dest": "section2", "params": {"param1": "value1"}, "meta": {"meta1": "value1"}, "on_return": {"return1": "value1"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_execute_instance(self):
        main_section = self.response.add_section('main')
        execute_instruction = Execute(dest="section2", params={"param1": "value1"}, meta={"meta1": "value1"},
                                      on_return={"return1": "value1"})
        main_section.add_instruction(execute_instruction)
        expected_swml = '{"sections": {"main": [{"execute": {"dest": "section2", "params": {"param1": "value1"}, "meta": {"meta1": "value1"}, "on_return": {"return1": "value1"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
