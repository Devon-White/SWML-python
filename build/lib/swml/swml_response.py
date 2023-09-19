from .swml_instructions import *
from typing import Optional, Union, List, Dict, Tuple, Any
import json
import yaml


class Section:
    def __init__(self):
        self.instructions: List[Union[Instruction, dict]] = []

    def add_instruction(self, instruction: Union[Instruction, dict]):
        if instruction:
            self.instructions.append(instruction)
        else:
            raise ValueError("You cannot pass a set of empty instructions. Please pass valid SWML instruction")

    def ai(self,
           voice: Optional[str] = None,
           prompt: Optional[Union[Dict[str, Any], AI.PromptParams]] = None,
           post_prompt: Optional[Union[Dict[str, Any], AI.PromptParams]] = None,
           post_prompt_url: Optional[str] = None,
           post_prompt_auth_user: Optional[str] = None,
           post_prompt_auth_password: Optional[str] = None,
           params: Optional[Union[Dict[str, Any], AI.AIParams]] = None,
           SWAIG: Optional[Union[Dict[str, Any], AI.SWAIGParams]] = None,
           hints: Optional[List[str]] = None,
           languages: Optional[Union[List[Dict[str, Any]], List[AI.LanguageParams]]] = None):
        self.add_instruction(AI(voice=voice,
                                prompt=prompt,
                                post_prompt=post_prompt,
                                post_prompt_url=post_prompt_url,
                                post_prompt_auth_user=post_prompt_auth_user,
                                post_prompt_auth_password=post_prompt_auth_password,
                                params=params,
                                SWAIG=SWAIG,
                                hints=hints,
                                languages=languages))

    # Statements

    def answer(self, max_duration: Optional[int] = None):
        self.add_instruction(Answer(max_duration=max_duration))

    def cond(self,
             when: str,
             then: List[Any],
             else_: List[Any]):
        self.add_instruction(Cond(when=when, then=then, else_=else_))

    def connect(self,
                from_number: Optional[str] = None,
                headers: Optional[Dict[str, str]] = None,
                codecs: Optional[str] = None,
                webrtc_media: Optional[bool] = None,
                session_timeout: Optional[int] = None,
                ringback: Optional[List[str]] = None,
                timeout: Optional[int] = None,
                max_duration: Optional[int] = None,
                answer_on_bridge: Optional[bool] = None,
                call_state_url: Optional[str] = None,
                call_state_events: Optional[List[str]] = None,
                result: Optional[Union[Dict, List]] = None,
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
                                     timeout=timeout,
                                     max_duration=max_duration,
                                     answer_on_bridge=answer_on_bridge,
                                     call_state_url=call_state_url,
                                     call_state_events=call_state_events,
                                     result=result,
                                     serial_parallel=serial_parallel,
                                     serial=serial,
                                     parallel=parallel,
                                     to_number=to_number))

    def denoise(self):
        self.add_instruction(Denoise())

    def execute(self,
                dest: str,
                params: Optional[Dict[str, Any]] = None,
                meta: Optional[Dict[str, Any]] = None,
                on_return: Optional[Dict[str, Any]] = None):
        self.add_instruction(Execute(dest=dest, params=params, meta=meta, on_return=on_return))

    def goto(self,
             label: str,
             when: Optional[str] = None,
             max_: Optional[int] = None,
             meta: Optional[Any] = None):
        self.add_instruction(Goto(label=label, when=when, max_=max_, meta=meta))

    def hangup(self, reason: Optional[str] = None):
        self.add_instruction(Hangup(reason=reason))

    def join_room(self, name: str):
        self.add_instruction(JoinRoom(name=name))

    def play(self,
             urls: Optional[List[str]] = None,
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

    def prompt(self,
               play: Union[str, List[str]],
               volume: Optional[float] = None,
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
               speech_hints: Optional[List[str]] = None,
               result: Optional[Union[dict, list]] = None):
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
                                    speech_hints=speech_hints,
                                    result=result))

    def receive_fax(self):
        self.add_instruction(ReceiveFax())

    def record(self,
               stereo: Optional[bool] = None,
               format_: Optional[str] = None,
               direction: Optional[str] = None,
               terminators: Optional[str] = None,
               beep: Optional[bool] = None,
               input_sensitivity: Optional[float] = None,
               initial_timeout: Optional[float] = None,
               end_silence_timeout: Optional[float] = None):
        self.add_instruction(Record(stereo=stereo,
                                    format_=format_,
                                    direction=direction,
                                    terminators=terminators,
                                    beep=beep,
                                    input_sensitivity=input_sensitivity,
                                    initial_timeout=initial_timeout,
                                    end_silence_timeout=end_silence_timeout))

    def record_call(self,
                    control_id: Optional[str] = None,
                    stereo: Optional[bool] = None,
                    format_: Optional[str] = None,
                    direction: Optional[str] = None,
                    terminators: Optional[str] = None,
                    beep: Optional[bool] = None,
                    input_sensitivity: Optional[float] = None,
                    initial_timeout: Optional[float] = None,
                    end_silence_timeout: Optional[float] = None):
        self.add_instruction(RecordCall(control_id=control_id,
                                        stereo=stereo,
                                        format_=format_,
                                        direction=direction,
                                        terminators=terminators,
                                        beep=beep,
                                        input_sensitivity=input_sensitivity,
                                        initial_timeout=initial_timeout,
                                        end_silence_timeout=end_silence_timeout))

    def request(self,
                url: str,
                method: str,
                headers:
                Optional[Dict[str, str]] = None,
                body: Optional[Union[str, Dict[str, Any]]] = None, timeout: Optional[float] = None,
                connect_timeout: Optional[float] = None, save_variables: Optional[bool] = False):
        self.add_instruction(Request(url=url, method=method, headers=headers, body=body, timeout=timeout,
                                     connect_timeout=connect_timeout, save_variables=save_variables))

    def return_(self, return_value: Optional[Any] = None):
        self.add_instruction(Return(return_value=return_value))

    def send_digits(self, digits: str):
        self.add_instruction(SendDigits(digits=digits))

    def send_fax(self, document: str, header_info: Optional[str] = None, identity: Optional[str] = None):
        self.add_instruction(SendFax(document=document, header_info=header_info, identity=identity))

    def send_sms(self,
                 to_number: str,
                 from_number: str,
                 body: str,
                 media: Optional[List[str]] = None,
                 region: Optional[str] = None,
                 tags: Optional[List[str]] = None):
        self.add_instruction(SendSMS(to_number=to_number, from_number=from_number, body=body, media=media, region=region, tags=tags))

    def set(self, variables: Dict[str, Any]):
        self.add_instruction(Set(variables=variables))

    def sip_refer(self, to_uri: str, result: Union[dict, list]):
        self.add_instruction(SipRefer(to_uri=to_uri, result=result))

    def stop_denoise(self):
        self.add_instruction(StopDenoise())

    def stop_record_call(self, control_id: Optional[str] = None):
        self.add_instruction(StopRecordCall(control_id=control_id))

    def stop_tap(self, control_id: str):
        self.add_instruction(StopTap(control_id=control_id))

    def switch(self,
               variable: str,
               case: Optional[Dict[str, list]] = None,
               default: Optional[List[Any]] = None):
        if case:
            for key, instructions in case.items():
                case[key] = [inst.to_dict() if isinstance(inst, Instruction) else inst for inst in instructions]
        if default:
            default = [inst.to_dict() if isinstance(inst, Instruction) else inst for inst in default]
        self.add_instruction(Switch(variable=variable, case=case, default=default))

    def tap(self,
            uri: str,
            control_id: Optional[str] = None,
            direction: Optional[str] = None,
            codec: Optional[str] = None,
            rtp_ptime: Optional[int] = None):
        self.add_instruction(Tap(uri=uri,
                                 control_id=control_id,
                                 direction=direction,
                                 codec=codec,
                                 rtp_ptime=rtp_ptime))

    def transfer(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 result: Optional[Union[dict, list]] = None):
        self.add_instruction(Transfer(dest=dest, params=params, meta=meta, result=result))

    def unset(self, _vars: Union[str, List[str]]):
        self.add_instruction(Unset(_vars=_vars))


class SWMLResponse:
    def __init__(self):
        self.sections: Dict[str, Section] = {}

    def __str__(self):
        return self.generate_swml()

    def add_section(self, section_name: str) -> Section:
        section = Section()
        self.sections[section_name] = section
        return section

    def generate_swml(self, format_: str = "json") -> str:
        # Check if the requested format is valid (either 'json' or 'yaml')
        if format_ not in ['json', 'yaml']:
            raise ValueError("Invalid format. Supported formats are 'json' and 'yaml'.")

        # Generate a dictionary where each key is a section name and each value is a list of instructions
        # For each instruction in the section, if it's an instance of the Instruction class, convert it to_number a dictionary using the to_dict() method
        # If the instruction is not an instance of the Instruction class, assume it's already a dictionary and add it directly
        sections_dict = {k: [(inst.to_dict() if isinstance(inst, Instruction) else inst) for inst in v.instructions] for
                         k, v in self.sections.items()}

        # Depending on the format parameter, serialize the dictionary to_number a JSON or YAML string and return it
        # If the format is 'json', use json.dumps() to_number convert the dictionary to_number a JSON string
        # If the format is 'yaml', use yaml.dump() to_number convert the dictionary to_number a YAML string
        return json.dumps({"sections": sections_dict}, sort_keys=False) if format_ == "json" else yaml.dump(
            {"sections": sections_dict}, sort_keys=False)
