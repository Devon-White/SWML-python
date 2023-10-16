from .swml_instructions import *
import json
import yaml


# Constants
SUPPORTED_FORMATS = ['json', 'yaml']


class CustomDumper(yaml.Dumper):
    pass


def represent_str(dumper, data):
    # Check if the string contains newlines
    if '\n' in data:
        # Use block literal style for multiline strings
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    else:
        # Use plain style for other strings
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=None)


# Register the custom representer for strings
CustomDumper.add_representer(str, represent_str)


class Section:
    def __init__(self):
        self.instructions: List[Union[Instruction, dict]] = []

    def add_instruction(self, instruction: Union[Instruction, dict]):
        if instruction:
            self.instructions.append(instruction)
        else:
            raise ValueError("You cannot pass a set of empty instructions. Please pass a valid SWML instruction.")

    def ai(self, voice=None, prompt=None, post_prompt=None, post_prompt_url=None, post_prompt_auth_user=None,
           post_prompt_auth_password=None, params=None, SWAIG=None, hints=None, languages=None, pronounce=None):
        self.add_instruction(AI(voice, prompt, post_prompt, post_prompt_url, post_prompt_auth_user,
                                post_prompt_auth_password, params, SWAIG, hints, languages, pronounce))

    def answer(self, max_duration=None):
        self.add_instruction(Answer(max_duration))

    def cond(self, when, then, else_):
        self.add_instruction(Cond(when, then, else_))

    def connect(self, from_number=None, headers=None, codecs=None, webrtc_media=None, session_timeout=None,
                ringback=None, timeout=None, max_duration=None, answer_on_bridge=None, call_state_url=None,
                call_state_events=None, result=None, serial_parallel=None, serial=None, parallel=None, to_number=None):
        self.add_instruction(Connect(from_number, headers, codecs, webrtc_media, session_timeout, ringback, timeout,
                                     max_duration, answer_on_bridge, call_state_url, call_state_events, result,
                                     serial_parallel, serial, parallel, to_number))

    def denoise(self):
        self.add_instruction(Denoise())

    def execute(self, dest, params=None, meta=None, on_return=None):
        self.add_instruction(Execute(dest, params, meta, on_return))

    def goto(self, label, when=None, max_=None, meta=None):
        self.add_instruction(Goto(label, when, max_, meta))

    def hangup(self, reason=None):
        self.add_instruction(Hangup(reason))

    def join_room(self, name):
        self.add_instruction(JoinRoom(name))

    def play(self, urls=None, url=None, volume=None, say_voice=None, silence=None, ring=None):
        self.add_instruction(Play(urls, url, volume, say_voice, silence, ring))

    def prompt(self, play, volume=None, say_voice=None, say_language=None, say_gender=None, max_digits=None,
               terminators=None, digit_timeout=None, initial_timeout=None, speech_timeout=None, speech_end_timeout=None,
               speech_language=None, speech_hints=None, result=None):
        self.add_instruction(Prompt(play, volume, say_voice, say_language, say_gender, max_digits, terminators,
                                    digit_timeout, initial_timeout, speech_timeout, speech_end_timeout, speech_language,
                                    speech_hints, result))

    def receive_fax(self):
        self.add_instruction(ReceiveFax())

    def record(self, stereo=None, format_=None, direction=None, terminators=None, beep=None, input_sensitivity=None,
               initial_timeout=None, end_silence_timeout=None):
        self.add_instruction(Record(stereo, format_, direction, terminators, beep, input_sensitivity, initial_timeout,
                                    end_silence_timeout))

    def record_call(self, control_id=None, stereo=None, format_=None, direction=None, terminators=None, beep=None,
                    input_sensitivity=None, initial_timeout=None, end_silence_timeout=None):
        self.add_instruction(RecordCall(control_id, stereo, format_, direction, terminators, beep, input_sensitivity,
                                        initial_timeout, end_silence_timeout))

    def request(self, url, method, headers=None, body=None, timeout=None, connect_timeout=None, save_variables=False):
        self.add_instruction(Request(url, method, headers, body, timeout, connect_timeout, save_variables))

    def return_(self, return_value: Optional[Any] = None):
        self.add_instruction(Return(return_value))

    def send_digits(self, digits):
        self.add_instruction(SendDigits(digits))

    def send_fax(self, document, header_info=None, identity=None):
        self.add_instruction(SendFax(document, header_info, identity))

    def send_sms(self, to_number, from_number, body, media=None, region=None, tags=None):

        params = {
            "to_number": f"{to_number}",
            "from_number": f"{from_number}",
            "body": body,
            "media": media,
            "region": region,
            "tags": tags
        }
        self.add_instruction(SendSMS(**params))

    def set(self, variables):
        self.add_instruction(Set(variables))

    def sip_refer(self, to_uri, result):
        self.add_instruction(SipRefer(to_uri, result))

    def stop_denoise(self):
        self.add_instruction(StopDenoise())

    def stop_record_call(self, control_id=None):
        self.add_instruction(StopRecordCall(control_id))

    def stop_tap(self, control_id):
        self.add_instruction(StopTap(control_id))

    def switch(self, variable, case=None, default=None):
        self.add_instruction(Switch(variable, case, default))

    def tap(self, uri, control_id=None, direction=None, codec=None, rtp_ptime=None):
        self.add_instruction(Tap(uri, control_id, direction, codec, rtp_ptime))

    def transfer(self, dest, params=None, meta=None, result=None):
        self.add_instruction(Transfer(dest, params, meta, result))

    def unset(self, _vars):
        self.add_instruction(Unset(_vars))


class SWMLResponse:
    def __init__(self):
        self.sections: Dict[str, Section] = {}

    def add_section(self, section_name: str) -> Section:
        section = Section()
        self.sections[section_name] = section
        return section

    def generate_swml(self, format_: str = "json") -> str:
        self._validate_format(format_)
        sections_dict = self._generate_sections_dict()
        return self._serialize(sections_dict, format_)

    @staticmethod
    def _validate_format(format_):
        """Validate the provided format."""
        if format_ not in SUPPORTED_FORMATS:
            raise ValueError(f"Invalid format. Supported formats are {', '.join(SUPPORTED_FORMATS)}.")

    def _generate_sections_dict(self) -> Dict[str, Any]:
        """Generate a dictionary representation of the sections."""
        return {
            k: [(inst.to_dict() if isinstance(inst, Instruction) else inst) for inst in v.instructions]
            for k, v in self.sections.items()
        }

    @staticmethod
    def _serialize(sections_dict: Dict[str, Any], format_: str) -> str:
        """Serialize the sections dictionary based on the specified format."""
        if format_ == "json":
            return json.dumps({"sections": sections_dict}, sort_keys=False)
        else:
            # Assuming yaml is the other format
            return yaml.dump({"sections": sections_dict}, sort_keys=False, default_flow_style=False, Dumper=CustomDumper, indent=2)

    def __str__(self):
        return self.generate_swml()
