from typing import Dict, Any, List, Optional, Union, Tuple
from collections import OrderedDict


class Instruction:
    def __init__(self, name: str, params: Dict[str, Any] = None):
        self.name = name
        self.params = params if params is not None else {}

    def to_dict(self):
        cleaned_params = []  # Use a list to preserve insertion order
        for k, v in self.params.items():
            if v is not None:
                if isinstance(v, BaseSWML):
                    cleaned_params.append((k, v.to_dict()))
                elif isinstance(v, list) and all(isinstance(x, BaseSWML) for x in v):
                    cleaned_params.append((k, [x.to_dict() for x in v]))
                elif isinstance(v, dict) and all(isinstance(x, BaseSWML) for x in v.values()):
                    cleaned_params.append((k, {k2: v2.to_dict() for k2, v2 in v.items()}))
                elif isinstance(v, list) and any(isinstance(x, BaseSWML) for x in v):
                    cleaned_params.append((k, [x.to_dict() if isinstance(x, BaseSWML) else x for x in v]))
                else:
                    cleaned_params.append((k, v))

        cleaned_params = dict(cleaned_params)

        if len(cleaned_params) == 1:
            # If there's only one parameter, return it as the value directly
            return {self.name: list(cleaned_params.values())[0]}
        elif cleaned_params:
            return {self.name: cleaned_params}
        else:
            return self.name





class BaseSWML(Instruction):
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.params = OrderedDict(kwargs)
        super().__init__(name, self.params)


class Answer(BaseSWML):
    def __init__(self, max_duration: Optional[int] = None):
        super().__init__("answer", max_duration=max_duration)

class Hangup(BaseSWML):
    def __init__(self, reason: Optional[str] = None):
        super().__init__("hangup", reason=reason)

class Prompt(BaseSWML):
    def __init__(self,
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
                 speech_hints: Optional[List[str]] = None):
        super().__init__("prompt", play=play, volume=volume, say_voice=say_voice, say_language=say_language,
                         say_gender=say_gender, max_digits=max_digits, terminators=terminators,
                         digit_timeout=digit_timeout, initial_timeout=initial_timeout, speech_timeout=speech_timeout,
                         speech_end_timeout=speech_end_timeout, speech_language=speech_language,
                         speech_hints=speech_hints)

class Play(BaseSWML):
    def __init__(self,
                 urls: Optional[Union[str, List[str]]] = None,
                 url: Optional[str] = None,
                 volume: Optional[float] = None,
                 say_voice: Optional[str] = None,
                 silence: Optional[float] = None,
                 ring: Optional[Tuple[float, str]] = None):
        if url is not None:
            if urls is None:
                urls = [url]
            elif isinstance(urls, list):
                urls.append(url)
            elif isinstance(urls, str):
                urls = [urls, url]
        super().__init__("play", urls=urls, volume=volume, say_voice=say_voice, silence=silence, ring=ring)


class Record(BaseSWML):
    def __init__(self,
                 stereo: Optional[bool] = None,
                 format: Optional[str] = None,
                 direction: Optional[str] = None,
                 terminators: Optional[str] = None,
                 beep: Optional[bool] = None,
                 input_sensitivity: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 end_silence_timeout: Optional[float] = None):
        super().__init__("record", stereo=stereo, format=format, direction=direction, terminators=terminators,
                         beep=beep, input_sensitivity=input_sensitivity, initial_timeout=initial_timeout,
                         end_silence_timeout=end_silence_timeout)

class RecordCall(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None,
                 stereo: Optional[bool] = None,
                 format: Optional[str] = None,
                 direction: Optional[str] = None,
                 terminators: Optional[str] = None,
                 beep: Optional[bool] = None,
                 input_sensitivity: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 end_silence_timeout: Optional[float] = None):
        super().__init__("record_call", control_id=control_id, stereo=stereo, format=format, direction=direction,
                         terminators=terminators, beep=beep, input_sensitivity=input_sensitivity,
                         initial_timeout=initial_timeout, end_silence_timeout=end_silence_timeout)

class StopRecordCall(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None):
        super().__init__("stop_record_call", control_id=control_id)

class JoinRoom(BaseSWML):
    def __init__(self, name: str):
        super().__init__("join_room", name=name)

class Denoise(BaseSWML):
    def __init__(self):
        super().__init__("denoise")

class StopDenoise(BaseSWML):
    def __init__(self):
        super().__init__("stop_denoise")

class ReceiveFax(BaseSWML):
    def __init__(self):
        super().__init__("receive_fax")

class SendFax(BaseSWML):
    def __init__(self,
                 document: str,
                 header_info: Optional[str] = None,
                 identity: Optional[str] = None):
        super().__init__("send_fax", document=document, header_info=header_info, identity=identity)

class SipRefer(BaseSWML):
    def __init__(self, to_uri: str):
        super().__init__("sip_refer", to_uri=to_uri)

class Connect(BaseSWML):
    def __init__(self,
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
        super().__init__("connect", from_number=from_number, headers=headers, codecs=codecs, webrtc_media=webrtc_media,
                         session_timeout=session_timeout, ringback=ringback, serial_parallel=serial_parallel,
                         serial=serial, parallel=parallel, to_number=to_number)

class Tap(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None,
                 audio_direction: Optional[str] = None,
                 target_type: Optional[str] = None,
                 target: Optional[str] = None):
        super().__init__("tap", control_id=control_id, audio_direction=audio_direction, target_type=target_type,
                         target=target)

class StopTap(BaseSWML):
    def __init__(self,
                 control_id: str):
        super().__init__("stop_tap", control_id=control_id)

class SendDigits(BaseSWML):
    def __init__(self,
                 digits: str,
                 duration_ms: Optional[int] = None):
        super().__init__("send_digits", digits=digits, duration_ms=duration_ms)

class SendSMS(BaseSWML):
    def __init__(self,
                 to: str,
                 from_: str,
                 body: str):
        super().__init__("send_sms", to=to, from_=from_, body=body)

class AI(BaseSWML):
    def __init__(self,
                 voice: Optional[str] = None,
                 prompt: Optional[Dict[str, Any]] = None,
                 post_prompt: Optional[Dict[str, Any]] = None,
                 post_prompt_url: Optional[str] = None,
                 post_prompt_auth_user: Optional[str] = None,
                 post_prompt_auth_password: Optional[str] = None,
                 SWAIG: Optional[List[Dict[str, Any]]] = None,
                 hints: Optional[List[str]] = None,
                 languages: Optional[List[Dict[str, Any]]] = None):
        super().__init__("ai", voice=voice, prompt=prompt, post_prompt=post_prompt, post_prompt_url=post_prompt_url,
                         post_prompt_auth_user=post_prompt_auth_user,
                         post_prompt_auth_password=post_prompt_auth_password, SWAIG=SWAIG, hints=hints,
                         languages=languages)

class Transfer(BaseSWML):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 meta: Optional[Dict[str, Any]] = None):
        super().__init__("transfer", dest=dest, params=params, meta=meta)


class Execute(BaseSWML):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 on_return: Optional[Dict[str, Any]] = None):
        super().__init__("execute", dest=dest, params=params, on_return=on_return)

class Return(BaseSWML):
    def __init__(self, return_value: Optional[Any] = None):
        super().__init__("return", return_value=return_value)

class Request(BaseSWML):
    def __init__(self,
                 url: str,
                 method: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: Optional[Union[str, Dict[str, Any]]] = None,
                 timeout: Optional[float] = 5.0,
                 connect_timeout: Optional[float] = 5.0,
                 save_variables: Optional[bool] = False):
        super().__init__("request",
                         url=url,
                         method=method,
                         headers=headers,
                         body=body,
                         timeout=timeout,
                         connect_timeout=connect_timeout,
                         save_variables=save_variables)

class Switch(BaseSWML):
    def __init__(self, variable: str, case: Optional[Dict[str or int, List[Any]]] = None, default: Optional[List[Any]] = None):
        case = self.convert_to_dict(case)
        default = self.convert_to_dict(default)
        super().__init__("switch", variable=variable, case=case, default=default)

    @staticmethod
    def convert_to_dict(value):
        if isinstance(value, BaseSWML):
            return value.to_dict()
        elif isinstance(value, list) and all(isinstance(x, BaseSWML) for x in value):
            return [x.to_dict() for x in value]
        elif isinstance(value, dict):
            return {key: [x.to_dict() for x in val] for key, val in value.items()}
        else:
            return value

class Cond(BaseSWML):
    def __init__(self, when: str, then: List[Any], else_: List[Any]):
        super().__init__("cond", when=when, then=then, else_=else_)

class Set(BaseSWML):
    def __init__(self, variables: Dict[str, Any]):
        super().__init__("set", variables=variables)

class Unset(BaseSWML):
    def __init__(self, vars: Union[str, List[str]]):
        super().__init__("unset", vars=vars)
