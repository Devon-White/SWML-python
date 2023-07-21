from swml import SWMLResponse, Record
import unittest


class TestSWMLRecord(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_record_method(self):
        main_section = self.response.add_section('main')
        main_section.record(
            stereo=True,
            format_="mp3",
            direction="both",
            terminators="#",
            beep=True,
            input_sensitivity=0.5,
            initial_timeout=5.0,
            end_silence_timeout=3.0
        )

        expected_swml = '{"sections": {"main": [{"record": {"stereo": true, "format": "mp3", "direction": "both", "terminators": "#", "beep": true, "input_sensitivity": 0.5, "initial_timeout": 5.0, "end_silence_timeout": 3.0}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_record_instance(self):
        main_section = self.response.add_section('main')
        main_section_record = Record(
            stereo=True,
            format_="mp3",
            direction="both",
            terminators="#",
            beep=True,
            input_sensitivity=0.5,
            initial_timeout=5.0,
            end_silence_timeout=3.0
        )
        main_section.add_instruction(main_section_record)

        expected_swml = '{"sections": {"main": [{"record": {"stereo": true, "format": "mp3", "direction": "both", "terminators": "#", "beep": true, "input_sensitivity": 0.5, "initial_timeout": 5.0, "end_silence_timeout": 3.0}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)
