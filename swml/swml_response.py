import dataclasses
from .swml_instructions import *
import json
import yaml

# Constants
SUPPORTED_FORMATS = ['json', 'yaml']

class Section:
    def __init__(self):
        self.instructions: List[Union[Instruction, dict]] = []

    def add_instruction(self, instruction: Union[Instruction, dict]):
        if instruction:
            self.instructions.append(instruction)
        else:
            raise ValueError("You cannot pass a set of empty instructions. Please pass a valid SWML instruction.")

    def ai(self, **kwargs):

        self.add_instruction(AI(**kwargs))

    def answer(self, **kwargs):
        self.add_instruction(Answer(**kwargs))

    def cond(self, **kwargs):
        self.add_instruction(Cond(**kwargs))

    def connect(self, **kwargs):
        self.add_instruction(Connect(**kwargs))

    def denoise(self):
        self.add_instruction(Denoise())

    def execute(self, **kwargs):
        self.add_instruction(Execute(**kwargs))

    def goto(self, **kwargs):
        self.add_instruction(Goto(**kwargs))

    def hangup(self, **kwargs):
        self.add_instruction(Hangup(**kwargs))

    def join_room(self, **kwargs):
        self.add_instruction(JoinRoom(**kwargs))

    def play(self, **kwargs):
        self.add_instruction(Play(**kwargs))

    def prompt(self, **kwargs):
        self.add_instruction(Prompt(**kwargs))

    def receive_fax(self):
        self.add_instruction(ReceiveFax())

    def record(self, **kwargs):
        self.add_instruction(Record(**kwargs))

    def record_call(self, **kwargs):
        self.add_instruction(RecordCall(**kwargs))

    def request(self, **kwargs):
        self.add_instruction(Request(**kwargs))

    def return_(self, return_value: Optional[Any] = None):
        self.add_instruction(Return(return_value=return_value))

    def send_digits(self, **kwargs):
        self.add_instruction(SendDigits(**kwargs))

    def send_fax(self, **kwargs):
        self.add_instruction(SendFax(**kwargs))

    def send_sms(self, **kwargs):
        self.add_instruction(SendSMS(**kwargs))

    def set(self, **kwargs):
        self.add_instruction(Set(**kwargs))

    def sip_refer(self, **kwargs):
        self.add_instruction(SipRefer(**kwargs))

    def stop_denoise(self):
        self.add_instruction(StopDenoise())

    def stop_record_call(self, **kwargs):
        self.add_instruction(StopRecordCall(**kwargs))

    def stop_tap(self, **kwargs):
        self.add_instruction(StopTap(**kwargs))

    def switch(self, **kwargs):
        self.add_instruction(Switch(**kwargs))

    def tap(self, **kwargs):
        self.add_instruction(Tap(**kwargs))

    def transfer(self, **kwargs):
        self.add_instruction(Transfer(**kwargs))

    def unset(self, **kwargs):
        self.add_instruction(Unset(**kwargs))


class SWMLResponse:
    def __init__(self):
        self.sections: Dict[str, Section] = {}

    def add_section(self, section_name: str) -> Section:
        section = Section()
        self.sections[section_name] = section
        return section

    def generate_swml(self, format_: str = "json") -> str:
        if format_ not in SUPPORTED_FORMATS:
            raise ValueError(f"Invalid format. Supported formats are {', '.join(SUPPORTED_FORMATS)}.")

        sections_dict = {k: [(inst.to_dict() if isinstance(inst, Instruction) else inst) for inst in v.instructions] for
                         k, v in self.sections.items()}

        return self._serialize(sections_dict, format_)

    @staticmethod
    def _serialize(sections_dict: Dict[str, Any], format_: str) -> str:
        if format_ == "json":
            return json.dumps({"sections": sections_dict}, sort_keys=False)
        else:
            return yaml.dump({"sections": sections_dict}, sort_keys=False)
