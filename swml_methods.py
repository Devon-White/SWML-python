# swml_methods.py

from typing import List, Optional, Dict, Any, Union, Tuple
from base_swml import BaseSWML


class Answer(BaseSWML):
    def __init__(self,
                 max_duration: Optional[int] = None):
        self.max_duration = max_duration


class Hangup(BaseSWML):
    def __init__(self, reason: Optional[str] = None):
        self.reason = reason


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
        self.play = play
        self.volume = volume
        self.say_voice = say_voice
        self.say_language = say_language
        self.say_gender = say_gender
        self.max_digits = max_digits
        self.terminators = terminators
        self.digit_timeout = digit_timeout
        self.initial_timeout = initial_timeout
        self.speech_timeout = speech_timeout
        self.speech_end_timeout = speech_end_timeout
        self.speech_language = speech_language
        self.speech_hints = speech_hints


class Play(BaseSWML):
    def __init__(
        self,
        urls: Optional[Union[str, List[str]]] = None,
        url: Optional[str] = None,
        volume: Optional[float] = None,
        say_voice: Optional[str] = None,
        silence: Optional[float] = None,
        ring: Optional[Tuple[float, str]] = None,
    ):
        self.volume = volume
        self.urls = self._validate_and_format_urls(urls, url, say_voice, silence, ring)

    @staticmethod
    def _validate_and_format_urls(urls, url, say_voice, silence, ring):
        result = []
        if url is None and urls is None:
            raise TypeError("A Play URL was not provided")
        if url:
            result.append(url)
        if urls:
            if isinstance(urls, list):
                result.extend(urls)
            else:
                result.append(urls)
        if say_voice:
            result.append(f"say:{say_voice}")
        if silence is not None:
            result.append(f"silence:{silence}")
        if ring:
            duration, tone = ring
            result.append(f"ring:{duration}:{tone}")
        return result if len(result) > 1 else result[0] if result else None

    def to_dict(self):
        dict_representation = super().to_dict()
        if isinstance(dict_representation, str):
            return dict_representation
        elif len(dict_representation) == 1 and "urls" in dict_representation:
            return dict_representation["urls"]
        return dict_representation



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
        self.stereo = stereo
        self.format = format
        self.direction = direction
        self.terminators = terminators
        self.beep = beep
        self.input_sensitivity = input_sensitivity
        self.initial_timeout = initial_timeout
        self.end_silence_timeout = end_silence_timeout


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
        self.control_id = control_id
        self.stereo = stereo
        self.format = format
        self.direction = direction
        self.terminators = terminators
        self.beep = beep
        self.input_sensitivity = input_sensitivity
        self.initial_timeout = initial_timeout
        self.end_silence_timeout = end_silence_timeout


class StopRecordCall(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None):
        self.control_id = control_id


class JoinRoom(BaseSWML):
    def __init__(self, name: str):
        self.name = name


class Denoise(BaseSWML):
    def __init__(self):
        pass


class StopDenoise(BaseSWML):
    def __init__(self):
        pass


class ReceiveFax(BaseSWML):
    def __init__(self):
        pass


class SendFax(BaseSWML):
    def __init__(self,
                 document: str,
                 header_info: Optional[str] = None,
                 identity: Optional[str] = None):
        self.document = document
        self.header_info = header_info
        self.identity = identity


class SipRefer(BaseSWML):
    def __init__(self, to_uri: str):
        self.to_uri = to_uri


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
        self.from_number = from_number
        self.headers = headers
        self.codecs = codecs
        self.webrtc_media = webrtc_media
        self.session_timeout = session_timeout
        self.ringback = ringback
        self.serial_parallel = serial_parallel
        self.serial = serial
        self.parallel = parallel
        self.to_number = to_number


class Tap(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None,
                 audio_direction: Optional[str] = None,
                 target_type: Optional[str] = None,
                 target: Optional[str] = None):
        self.control_id = control_id
        self.audio_direction = audio_direction
        self.target_type = target_type
        self.target = target


class StopTap(BaseSWML):
    def __init__(self,
                 control_id: str):
        self.control_id = control_id


class SendDigits(BaseSWML):
    def __init__(self,
                 digits: str,
                 duration_ms: Optional[int] = None):
        self.digits = digits
        self.duration_ms = duration_ms


class SendSMS(BaseSWML):
    def __init__(self,
                 to: str,
                 from_: str,
                 body: str):
        self.to = to
        self.from_ = from_
        self.body = body


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
        self.voice = voice
        self.prompt = prompt
        self.post_prompt = post_prompt
        self.post_prompt_url = post_prompt_url
        self.post_prompt_auth_user = post_prompt_auth_user
        self.post_prompt_auth_password = post_prompt_auth_password
        self.SWAIG = SWAIG
        self.hints = hints
        self.languages = languages
