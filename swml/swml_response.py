from .swml_instructions import *
from typing import Optional, Union, List, Dict, Tuple, Any
import json
import yaml



class Section:
    def __init__(self):
        self.instructions: List[Instruction] = []

    def add_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)

    def answer(self, max_duration: Optional[int] = None):
        self.add_instruction(Answer(max_duration=max_duration))

    def hangup(self, reason: Optional[str] = None):
        self.add_instruction(Hangup(reason=reason))

    def prompt(self, play: Union[str, List[str]], volume: Optional[float] = None,
               say_voice: Optional[str] = None,
               say_language: Optional[str] = None,
               say_gender: Optional[str] = None,
               max_digits: Optional[int] = None,
               terminators: Optional[str] = None,
               digit_timeout: Optional[float] = None,
               initial_timeout: Optional[float] = None,
               speech_timeout: Optional[float] = None,
               speech_end_timeout: Optional[float] = None,
               speech_language: Optional[str] = None,
               speech_hints: Optional[List[str]] = None):
        self.add_instruction(Prompt(play=play,
                                    volume=volume,
                                    say_voice=say_voice,
                                    say_language=say_language,
                                    say_gender=say_gender,
                                    max_digits=max_digits,
                                    terminators=terminators,
                                    digit_timeout=digit_timeout,
                                    initial_timeout=initial_timeout,
                                    speech_timeout=speech_timeout,
                                    speech_end_timeout=speech_end_timeout,
                                    speech_language=speech_language,
                                    speech_hints=speech_hints))

    def play(self,
             urls: Optional[Union[str, List[str]]] = None,
             url: Optional[str] = None,
             volume: Optional[float] = None,
             say_voice: Optional[str] = None,
             silence: Optional[float] = None,
             ring: Optional[Tuple[float, str]] = None):
        self.add_instruction(Play(urls=urls,
                                  url=url,
                                  volume=volume,
                                  say_voice=say_voice,
                                  silence=silence,
                                  ring=ring))

    def record(self,
               stereo: Optional[bool] = None,
               format: Optional[str] = None,
               direction: Optional[str] = None,
               terminators: Optional[str] = None,
               beep: Optional[bool] = None,
               input_sensitivity: Optional[float] = None,
               initial_timeout: Optional[float] = None,
               end_silence_timeout: Optional[float] = None):
        self.add_instruction(Record(stereo=stereo,
                                    format=format,
                                    direction=direction,
                                    terminators=terminators,
                                    beep=beep,
                                    input_sensitivity=input_sensitivity,
                                    initial_timeout=initial_timeout,
                                    end_silence_timeout=end_silence_timeout))

    def record_call(self,
                    control_id: Optional[str] = None,
                    stereo: Optional[bool] = None,
                    format: Optional[str] = None,
                    direction: Optional[str] = None,
                    terminators: Optional[str] = None,
                    beep: Optional[bool] = None,
                    input_sensitivity: Optional[float] = None,
                    initial_timeout: Optional[float] = None,
                    end_silence_timeout: Optional[float] = None):
        self.add_instruction(RecordCall(control_id=control_id,
                                        stereo=stereo,
                                        format=format,
                                        direction=direction,
                                        terminators=terminators,
                                        beep=beep,
                                        input_sensitivity=input_sensitivity,
                                        initial_timeout=initial_timeout,
                                        end_silence_timeout=end_silence_timeout))

    def stop_record_call(self, control_id: Optional[str] = None):
        self.add_instruction(StopRecordCall(control_id=control_id))

    def join_room(self, name: str):
        self.add_instruction(JoinRoom(name=name))

    def denoise(self):
        self.add_instruction(Denoise())

    def stop_denoise(self):
        self.add_instruction(StopDenoise())

    def receive_fax(self):
        self.add_instruction(ReceiveFax())

    def send_fax(self, document: str, header_info: Optional[str] = None, identity: Optional[str] = None):
        self.add_instruction(SendFax(document=document, header_info=header_info, identity=identity))

    def sip_refer(self, to_uri: str):
        self.add_instruction(SipRefer(to_uri=to_uri))

    def connect(self,
                from_number: Optional[str] = None,
                headers: Optional[Dict[str, str]] = None,
                codecs: Optional[str] = None,
                webrtc_media: Optional[bool] = None,
                session_timeout: Optional[int] = None,
                ringback: Optional[List[str]] = None,
                serial_parallel: Optional[List[List[Dict[str, str]]]] = None,
                serial: Optional[List[Dict[str, str]]] = None,
                parallel: Optional[List[Dict[str, str]]] = None,
                to_number: Optional[str] = None):
        self.add_instruction(Connect(from_number=from_number,
                                     headers=headers,
                                     codecs=codecs,
                                     webrtc_media=webrtc_media,
                                     session_timeout=session_timeout,
                                     ringback=ringback,
                                     serial_parallel=serial_parallel,
                                     serial=serial,
                                     parallel=parallel,
                                     to_number=to_number))

    def tap(self,
            control_id: Optional[str] = None,
            audio_direction: Optional[str] = None,
            target_type: Optional[str] = None,
            target: Optional[str] = None):
        self.add_instruction(Tap(control_id=control_id,
                                 audio_direction=audio_direction,
                                 target_type=target_type,
                                 target=target))

    def stop_tap(self, control_id: str):
        self.add_instruction(StopTap(control_id=control_id))

    def send_digits(self, digits: str, duration_ms: Optional[int] = None):
        self.add_instruction(SendDigits(digits=digits, duration_ms=duration_ms))

    def send_sms(self, to: str, from_: str, body: str):
        self.add_instruction(SendSMS(to=to, from_=from_, body=body))

    def ai(self,
           voice: Optional[str] = None,
           prompt: Optional[Dict[str, Any]] = None,
           post_prompt: Optional[Dict[str, Any]] = None,
           post_prompt_url: Optional[str] = None,
           post_prompt_auth_user: Optional[str] = None,
           post_prompt_auth_password: Optional[str] = None,
           SWAIG: Optional[List[Dict[str, Any]]] = None,
           hints: Optional[List[str]] = None,
           languages: Optional[List[Dict[str, Any]]] = None):
        self.add_instruction(AI(voice=voice,
                                prompt=prompt,
                                post_prompt=post_prompt,
                                post_prompt_url=post_prompt_url,
                                post_prompt_auth_user=post_prompt_auth_user,
                                post_prompt_auth_password=post_prompt_auth_password,
                                SWAIG=SWAIG,
                                hints=hints,
                                languages=languages))

    # Statements

    def transfer(self, dest: str, params: Optional[Dict[str, Any]] = None, meta: Optional[Dict[str, Any]] = None):
        self.add_instruction(Transfer(dest=dest, params=params, meta=meta))

    def execute(self, dest: str, params: Optional[Dict[str, Any]] = None, on_return: Optional[Dict[str, Any]] = None):
        self.add_instruction(Execute(dest=dest, params=params, on_return=on_return))

    def return_(self, return_value: Optional[Any] = None):
        self.add_instruction(Return(return_value=return_value))

    def request(self, url: str, method: str, headers: Optional[Dict[str, str]] = None,
                body: Optional[Union[str, Dict[str, Any]]] = None, timeout: Optional[float] = 5.0,
                connect_timeout: Optional[float] = 5.0, save_variables: Optional[bool] = False):
        self.add_instruction(Request(url=url, method=method, headers=headers, body=body, timeout=timeout,
                                     connect_timeout=connect_timeout, save_variables=save_variables))

    def switch(self, variable: str, case: Optional[Dict[str, List[Any]]] = None, default: Optional[List[Any]] = None):
        if case is not None:
            for key, instructions in case.items():
                case[key] = [inst.to_dict() if isinstance(inst, Instruction) else inst for inst in instructions]
        if default is not None:
            default = [inst.to_dict() if isinstance(inst, Instruction) else inst for inst in default]
        self.add_instruction(Switch(variable=variable, case=case, default=default))

    def cond(self, when: str, then: List[Any], else_: List[Any]):
        self.add_instruction(Cond(when=when, then=then, else_=else_))

    def set(self, variables: Dict[str, Any]):
        self.add_instruction(Set(variables=variables))

    def unset(self, vars: Union[str, List[str]]):
        self.add_instruction(Unset(vars=vars))


class SWMLResponse:
    def __init__(self):
        self.sections: Dict[str, Section] = {}

    def add_section(self, section_name: str) -> Section:
        section = Section()
        self.sections[section_name] = section
        return section

    def generate_swml(self, format: str = "json") -> str:
        sections_dict = {}
        for k, v in self.sections.items():
            instructions = []
            for inst in v.instructions:
                instructions.append(inst.to_dict())
            sections_dict[k] = instructions

        if format == "json":
            return json.dumps({"sections": sections_dict}, sort_keys=False, indent=4)
        elif format == "yaml":
            return yaml.dump({"sections": sections_dict}, sort_keys=False, indent=4)
        else:
            raise ValueError("Invalid format. Supported formats are 'json' and 'yaml'.")

    def __str__(self):
        return self.generate_swml()
