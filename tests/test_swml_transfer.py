import unittest
from swml import SWMLResponse, Transfer

class TestSWMLTransfer(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_transfer_method(self):
        main_section = self.response.add_section('main')
        main_section.transfer(dest="sip:test@domain.com", params={"param1": "value1"}, meta={"meta1": "value1"}, result={"result1": "value1"})
        expected_swml = '{"sections": {"main": [{"transfer": {"dest": "sip:test@domain.com", "params": {"param1": "value1"}, "meta": {"meta1": "value1"}, "result": {"result1": "value1"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_transfer_instance(self):
        main_section = self.response.add_section('main')
        transfer_instruction = Transfer(dest="sip:test@domain.com", params={"param1": "value1"}, meta={"meta1": "value1"}, result={"result1": "value1"})
        main_section.add_instruction(transfer_instruction)
        expected_swml = '{"sections": {"main": [{"transfer": {"dest": "sip:test@domain.com", "params": {"param1": "value1"}, "meta": {"meta1": "value1"}, "result": {"result1": "value1"}}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
