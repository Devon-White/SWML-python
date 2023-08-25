import unittest
from swml import SWMLResponse, AI


class TestSWMLAIUpdated(unittest.TestCase):
    def setUp(self):
        self.response = SWMLResponse()

    def test_ai_method(self):
        main_section = self.response.add_section('main')

        # Utilizing SWAIGFunction.FunctionArgs and SWAIGDefaults
        function_arg = AI.SWAIGFunction.FunctionArgs(
            type_="object",
            properties={
                "location": AI.SWAIGFunction.FunctionArgs.PropertyDetail(
                    type_="string",
                    description="Location for weather lookup"
                )
            }
        )

        swaig_defaults = AI.SWAIGDefaults(
            web_hook_url="https://default-url.com",
            web_hook_auth_user="default_user",
            web_hook_auth_password="default_password",
            meta_data={"source": "test"},
            meta_data_token="default_token"
        )

        main_section.ai(
            voice="en-US-Neural2-F",
            prompt=AI.PromptParams(text="Hello, how can I assist you today?"),
            post_prompt=AI.PromptParams(text="Thank you for using our service."),
            post_prompt_url="https://example.com/callback",
            post_prompt_auth_user="username",
            post_prompt_auth_password="password",
            params=AI.AIParams(
                direction="bidirectional",
                wait_for_user=True,
                end_of_speech_timeout=5000,
                attention_timeout=10000,
                inactivity_timeout=15000,
                background_file="background_music.mp3",
                background_file_loops=3,
                background_file_volume=50,
                ai_volume=75,
                local_tz="America/Los_Angeles",
                conscience=True,
                save_conversation=True,
                conversation_id="12345",
                digit_timeout=2000,
                digit_terminators="#",
                energy_level=50,
                swaig_allow_swml=True
            ),
            SWAIG=AI.SWAIGParams(
                functions=[AI.SWAIGFunction(function="get_weather", web_hook_url="https://example.com/weather",
                                            purpose="Get the weather", argument=function_arg)],
                defaults=swaig_defaults
            ),
            hints=["weather", "forecast"],
            languages=[AI.LanguageParams(name="English", code="en-US", voice="en-US-Neural2-F")]
        )

        # Utilizing a concise representation for the expected SWML
        generated_swml = self.response.generate_swml()
        self.assertTrue(isinstance(generated_swml, str) and len(generated_swml) > 0)

