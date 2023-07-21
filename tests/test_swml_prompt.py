from swml import Prompt, SWMLResponse
import unittest

class TestSWMLPrompt(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_prompt_method(self):
        main_section = self.response.add_section('main')
        main_section.prompt(
            play="say:Please say an input",
            say_language="en-US",
            max_digits=1,
            terminators="#",
            digit_timeout=2.5,
            initial_timeout=5.0,
            speech_timeout=2.0,
            speech_end_timeout=1.0,
            speech_language="en-US",
            speech_hints=["one", "two", "three"]
        )

        expected_swml = '{"sections": {"main": [{"prompt": {"play": "say:Please say an input", "say_language": "en-US", "max_digits": 1, "terminators": "#", "digit_timeout": 2.5, "initial_timeout": 5.0, "speech_timeout": 2.0, "speech_end_timeout": 1.0, "speech_language": "en-US", "speech_hints": ["one", "two", "three"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

    def test_add_instruction_with_prompt_instance(self):
        main_section = self.response.add_section('main')
        main_section_prompt = Prompt(
            play="say:Please say an input",
            say_language="en-US",
            max_digits=1,
            terminators="#",
            digit_timeout=2.5,
            initial_timeout=5.0,
            speech_timeout=2.0,
            speech_end_timeout=1.0,
            speech_language="en-US",
            speech_hints=["one", "two", "three"]
        )
        main_section.add_instruction(main_section_prompt)

        expected_swml = '{"sections": {"main": [{"prompt": {"play": "say:Please say an input", "say_language": "en-US", "max_digits": 1, "terminators": "#", "digit_timeout": 2.5, "initial_timeout": 5.0, "speech_timeout": 2.0, "speech_end_timeout": 1.0, "speech_language": "en-US", "speech_hints": ["one", "two", "three"]}}]}}'
        self.assertEqual(self.response.generate_swml(), expected_swml)

