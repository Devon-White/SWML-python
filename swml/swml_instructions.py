from typing import List, Dict, Union, Optional, Any, Tuple
from collections import OrderedDict
import json


def find_sets_in_dict(d, path=[]):
    for k, v in d.items():
        current_path = path + [k]
        if isinstance(v, set):
            print(f"Found set at path: {' -> '.join(map(str, current_path))}, Value: {v}")
        elif isinstance(v, dict):
            find_sets_in_dict(v, current_path)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if hasattr(obj, '__dict__'):
            return {key: value for key, value in obj.__dict__.items() if value is not None}
        return super().default(obj)


# Instruction Class
class Instruction:
    def __init__(self, swml_name: str, swml_params: Dict[str, Any] = None):
        self.swml_name = swml_name
        self.swml_params = swml_params if swml_params is not None else {}

    def to_dict(self):
        cleaned_params = {key: value for key, value in self.swml_params.items() if value is not None}

        # Handle Action objects in the cleaned_params
        for k, v in cleaned_params.items():
            if isinstance(k, set):
                print(f"Key with set value: {k}, Value: {v}")
            if isinstance(v, list) and all(isinstance(item, Action) for item in v):
                cleaned_params[k] = [item.__dict__ for item in v]

        return {self.swml_name: json.loads(
            json.dumps(cleaned_params, cls=CustomJSONEncoder))} if cleaned_params else self.swml_name


# BaseSWML Class
class BaseSWML(Instruction):
    def __init__(self, swml_name: str, **kwargs):
        self.swml_name = swml_name
        self.swml_params = OrderedDict(kwargs)
        super().__init__(swml_name, self.swml_params)


# Action Classes
class Action:
    pass


class SWML(Action):
    def __init__(self, swml_object: Dict[str, Any]):
        self.swml_object = swml_object


class Say(Action):
    def __init__(self, message: str):
        self.message = message


class Stop(Action):
    def __init__(self, stop: bool = True):
        self.stop = stop


class ToggleFunctions(Action):
    def __init__(self, active: bool = True, functions: List[str] = None):
        self.active = active
        self.functions = functions if functions else []


class BackToBackFunctions(Action):
    def __init__(self, back_to_back: bool = False):
        self.back_to_back = back_to_back


class SetMetaData(Action):
    def __init__(self, meta_data: Dict[str, Any]):
        self.meta_data = meta_data


class PlaybackBG(Action):
    def __init__(self, file: str, wait: bool = False):
        self.file = file
        self.wait = wait


class StopPlaybackBG(Action):
    def __init__(self, stop_playback: bool = True):
        self.stop_playback = stop_playback


class UserInput(Action):
    def __init__(self, input_text: str):
        self.input_text = input_text


# LanguageParams Class
class LanguageParams:
    def __init__(self, name: Optional[str] = None,
                 code: Optional[str] = None,
                 voice: Optional[str] = None,
                 fillers: Optional[List[str]] = None):
        self.name = name
        self.code = code
        self.voice = voice
        self.fillers = fillers


class Pronounce:
    def __init__(self,
                 replace: str,
                 with_: str,
                 ignore_case: Optional[bool] = True):
        params = {"replace": replace, "with": with_, "ignore_case": ignore_case}
        super().__init__("pronounce", **params)


# PromptParams Class
class PromptParams:
    def __init__(self,
                 text: Optional[str] = None,
                 language: Optional[str] = None,
                 temperature: Optional[float] = None,
                 top_p: Optional[float] = None,
                 confidence: Optional[float] = None,
                 presence_penalty: Optional[float] = None,
                 frequency_penalty: Optional[float] = None,
                 result: Optional[Union[Dict[str, Any], List[Any]]] = None):
        self.text = text
        self.language = language
        self.temperature = temperature
        self.top_p = top_p
        self.confidence = confidence
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.result = result


# DataMapExpression Class
class DataMapExpression:
    class DataMapExpressionOutput:
        def __init__(self, response: Optional[str] = None,
                     action: Union[Optional[List[Action]], Dict[str, Any]] = None):
            self.response = response
            self.action = action

    def __init__(self, string: str, pattern: str, output: Union[DataMapExpressionOutput, Dict[str, Any]]):
        self.string = string
        self.pattern = pattern
        self.output = output


# DataMapWebhook Class
class DataMapWebhook:
    class DataMapWebhookOutput:
        def __init__(self, response: Optional[str] = None,
                     action: Union[Optional[List[Action]], Dict[str, Any]] = None):
            self.response = response
            self.action = action

    def __init__(self, url: str, headers: Dict[str, str], method: str,
                 output: Union[DataMapWebhookOutput, Dict[str, Any]]):
        self.url = url
        self.headers = headers
        self.method = method
        self.output = output


# DataMap Class
class DataMap:
    Expressions = DataMapExpression
    Webhooks = DataMapWebhook

    def __init__(self, expressions: Union[Optional[List[DataMapExpression]], Optional[List]] = None,
                 webhooks: Union[Optional[List[DataMapWebhook]], Optional[List]] = None):
        self.expressions = expressions if expressions else None
        self.webhooks = webhooks if webhooks else None


# SWAIGFunction Class
class SWAIGFunction:
    DataMap = DataMap

    class FunctionArgs:
        class PropertyDetail(Instruction):  # Inherit from Instruction
            def __init__(self,
                         type_: Optional[str] = None,
                         description: Optional[str] = None):
                super().__init__("property_detail", {"type": type_, "description": description})

            def to_dict(self):
                return self.swml_params  # Return the serialized swml_params

        def __init__(self,
                     type_: str,
                     properties: Optional[Dict[str, PropertyDetail]] = None):
            self.type = type_
            self.properties = properties if properties else {}

    def __init__(self,
                 function: str,
                 purpose: str,
                 web_hook_url: Optional[str] = None,
                 web_hook_auth_user: Optional[str] = None,
                 web_hook_auth_pass: Optional[str] = None,
                 argument: Union[Optional[Dict[str, Any]], Optional[FunctionArgs]] = None,
                 data_map: Union[Optional[Dict[str, Any]], Optional[DataMap]] = None,
                 **kwargs):
        self.function = function
        self.web_hook_url = web_hook_url
        self.web_hook_auth_user = web_hook_auth_user
        self.web_hook_auth_pass = web_hook_auth_pass
        self.purpose = purpose
        self.argument = argument
        self.data_map = data_map

        # Setting instance variables based on kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


# SWAIGDefaults Class
class SWAIGDefaults:
    def __init__(self,
                 web_hook_url: Optional[str] = None,
                 web_hook_auth_user: Optional[str] = None,
                 web_hook_auth_password: Optional[str] = None,
                 meta_data: Optional[Dict[str, Any]] = None,
                 meta_data_token: Optional[str] = None):
        self.web_hook_url = web_hook_url
        self.web_hook_auth_user = web_hook_auth_user
        self.web_hook_auth_password = web_hook_auth_password
        self.meta_data = meta_data
        self.meta_data_token = meta_data_token


# SWAIGParams Class
class SWAIGParams:
    def __init__(self,
                 functions: Optional[Union[List[SWAIGFunction], List[Dict[str, Any]]]] = None,
                 defaults: Optional[Union[SWAIGDefaults, Dict[str, Any]]] = None,
                 native_functions: Optional[List[str]] = None,
                 includes: Optional[List[Dict[str, Any]]] = None):
        self.functions = functions
        self.defaults = defaults
        self.native_functions = native_functions
        self.includes = includes


# AIParams Class
class AIParams:
    def __init__(self,
                 direction: Optional[str] = None,
                 wait_for_user: Optional[bool] = None,
                 end_of_speech_timeout: Optional[int] = None,
                 attention_timeout: Optional[int] = None,
                 inactivity_timeout: Optional[int] = None,
                 background_file: Optional[str] = None,
                 background_file_loops: Optional[int] = None,
                 background_file_volume: Optional[int] = None,
                 ai_volume: Optional[int] = None,
                 local_tz: Optional[str] = None,
                 conscience: Optional[bool] = None,
                 save_conversation: Optional[bool] = None,
                 conversation_id: Optional[str] = None,
                 digit_timeout: Optional[int] = None,
                 digit_terminators: Optional[str] = None,
                 energy_level: Optional[int] = None,
                 swaig_allow_swml: Optional[bool] = None):
        self.direction = direction
        self.wait_for_user = wait_for_user
        self.end_of_speech_timeout = end_of_speech_timeout
        self.attention_timeout = attention_timeout
        self.inactivity_timeout = inactivity_timeout
        self.background_file = background_file
        self.background_file_loops = background_file_loops
        self.background_file_volume = background_file_volume
        self.ai_volume = ai_volume
        self.local_tz = local_tz
        self.conscience = conscience
        self.save_conversation = save_conversation
        self.conversation_id = conversation_id
        self.digit_timeout = digit_timeout
        self.digit_terminators = digit_terminators
        self.energy_level = energy_level
        self.swaig_allow_swml = swaig_allow_swml


# AI Class
class AI(BaseSWML):
    PromptParams = PromptParams
    SWAIGFunction = SWAIGFunction
    SWAIGParams = SWAIGParams
    SWAIGDefaults = SWAIGDefaults
    AIParams = AIParams
    LanguageParams = LanguageParams
    Pronounce = Pronounce

    def __init__(self,
                 voice: Optional[str] = None,
                 prompt: Optional[Union[Dict[str, Any], PromptParams]] = None,
                 post_prompt: Optional[Dict[str, Any]] = None,
                 post_prompt_url: Optional[str] = None,
                 post_prompt_auth_user: Optional[str] = None,
                 post_prompt_auth_password: Optional[str] = None,
                 params: Optional[Union[Dict[str, Any], AIParams]] = None,
                 SWAIG: Optional[Union[Dict[str, Any], SWAIGParams]] = None,
                 hints: Optional[List[str]] = None,
                 languages: Optional[List[Dict[str, Any]]] = None,
                 pronounce: Union[Optional[Dict[str, Any]], Pronounce] = None):
        super().__init__("ai", voice=voice, prompt=prompt, post_prompt=post_prompt, post_prompt_url=post_prompt_url,
                         post_prompt_auth_user=post_prompt_auth_user,
                         post_prompt_auth_password=post_prompt_auth_password,
                         params=params, SWAIG=SWAIG, hints=hints,
                         languages=languages, pronounce=pronounce)


class Answer(BaseSWML):
    def __init__(self, max_duration: Optional[int] = None):
        super().__init__("answer", max_duration=max_duration)


class Cond(BaseSWML):
    def __init__(self,
                 when: str,
                 then: List[Any],
                 else_: List[Any]):
        params = {"when": when, "then": then, "else": else_}
        super().__init__("cond", **params)


class Connect(BaseSWML):
    def __init__(self,
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
                 to_number: Optional[str] = None,
                 ):
        dialing_params = [serial_parallel, serial, parallel, to_number]
        if sum(param is not None for param in dialing_params) != 1:
            raise ValueError(
                "Exactly one of the dialing parameters (serial_parallel, serial, parallel, to_number) must be provided.")

        params = {
            "from": from_number,
            "headers": headers,
            "codecs": codecs,
            "webrtc_media": webrtc_media,
            "session_timeout": session_timeout,
            "ringback": ringback,
            "timeout": timeout,
            "max_duration": max_duration,
            "answer_on_bridge": answer_on_bridge,
            "call_state_url": call_state_url,
            "call_state_events": call_state_events,
            "result": result,
            "serial_parallel": serial_parallel,
            "serial": serial,
            "parallel": parallel,
            "to": to_number
        }

        super().__init__("connect", **params)


class Denoise(BaseSWML):
    def __init__(self):
        super().__init__("denoise")


class Execute(BaseSWML):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 on_return: Optional[Dict[str, Any]] = None):
        super().__init__("execute", dest=dest, params=params, meta=meta, on_return=on_return)


class Goto(BaseSWML):
    def __init__(self,
                 label: str,
                 when: Optional[str] = None,
                 max_: Optional[int] = None,
                 meta: Optional[Any] = None):
        if max_ is not None and (max_ < 1 or max_ > 100):
            raise ValueError("max_ must be between 1 and 100")
        params = {'label': label, 'when': when, "max": max_, 'meta': meta}
        super().__init__("goto", **params)


class Hangup(BaseSWML):
    def __init__(self, reason: Optional[str] = None):
        super().__init__("hangup", reason=reason)

        if reason is not None and reason not in ['busy', 'hangup', 'decline']:
            raise ValueError("Hangup reason must be one of the following: 'hangup', 'busy', or 'decline'")


class JoinRoom(BaseSWML):
    def __init__(self, name: str):
        super().__init__("join_room", name=name)


class Play(BaseSWML):
    def __init__(self,
                 urls: Optional[List[str]] = None,
                 url: Optional[str] = None,
                 volume: Optional[float] = None,
                 say_voice: Optional[str] = None,
                 silence: Optional[float] = None,
                 ring: Optional[Tuple[float, str]] = None):
        if url is not None and urls is not None:
            raise ValueError("Cannot provide both 'url' and 'urls'. Please provide only one.")
        elif url is not None:
            super().__init__("play", url=url, volume=volume, say_voice=say_voice, silence=silence, ring=ring)
        else:
            super().__init__("play", urls=urls, volume=volume, say_voice=say_voice, silence=silence, ring=ring)


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
                 speech_hints: Optional[List[str]] = None,
                 result: Optional[Union[dict, list]] = None):
        super().__init__("prompt", play=play, volume=volume, say_voice=say_voice, say_language=say_language,
                         say_gender=say_gender, max_digits=max_digits, terminators=terminators,
                         digit_timeout=digit_timeout, initial_timeout=initial_timeout, speech_timeout=speech_timeout,
                         speech_end_timeout=speech_end_timeout, speech_language=speech_language,
                         speech_hints=speech_hints, result=result)


class ReceiveFax(BaseSWML):
    def __init__(self):
        super().__init__("receive_fax")


class Record(BaseSWML):
    def __init__(self,
                 stereo: Optional[bool] = None,
                 format_: Optional[str] = None,
                 direction: Optional[str] = None,
                 terminators: Optional[str] = None,
                 beep: Optional[bool] = None,
                 input_sensitivity: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 end_silence_timeout: Optional[float] = None):
        params = {
            "stereo": stereo,
            "format": format_,
            "direction": direction,
            "terminators": terminators,
            "beep": beep,
            "input_sensitivity": input_sensitivity,
            "initial_timeout": initial_timeout,
            "end_silence_timeout": end_silence_timeout
        }
        super().__init__("record", **params)


class RecordCall(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None,
                 stereo: Optional[bool] = None,
                 format_: Optional[str] = None,
                 direction: Optional[str] = None,
                 terminators: Optional[str] = None,
                 beep: Optional[bool] = None,
                 input_sensitivity: Optional[float] = None,
                 initial_timeout: Optional[float] = None,
                 end_silence_timeout: Optional[float] = None):
        params = {
            "control_id": control_id,
            "stereo": stereo,
            "format": format_,
            "direction": direction,
            "terminators": terminators,
            "beep": beep,
            "input_sensitivity": input_sensitivity,
            "initial_timeout": initial_timeout,
            "end_silence_timeout": end_silence_timeout
        }
        super().__init__("record_call", **params)


class Request(BaseSWML):
    def __init__(self,
                 url: str,
                 method: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: Optional[Union[str, Dict[str, Any]]] = None,
                 timeout: Optional[float] = None,
                 connect_timeout: Optional[float] = None,
                 save_variables: Optional[bool] = False):
        params = {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
            "timeout": timeout,
            "connect_timeout": connect_timeout
        }
        if save_variables:
            params["save_variables"] = save_variables
        super().__init__("request", **params)


class Return(BaseSWML):
    def __init__(self, return_value: Optional[Any] = None):
        super().__init__("return", return_value=return_value)


class SendDigits(BaseSWML):
    def __init__(self,
                 digits: str):
        super().__init__("send_digits", digits=digits)


class SendFax(BaseSWML):
    def __init__(self,
                 document: str,
                 header_info: Optional[str] = None,
                 identity: Optional[str] = None):
        super().__init__("send_fax", document=document, header_info=header_info, identity=identity)


class SendSMS(BaseSWML):
    def __init__(self,
                 to_number: str,
                 from_number: str,
                 body: str,
                 media: Optional[List[str]] = None,
                 region: Optional[str] = None,
                 tags: Optional[List[str]] = None):
        super().__init__("send_sms", to_number=to_number, from_number=from_number, body=body, media=media,
                         region=region, tags=tags)


class Set(BaseSWML):
    def __init__(self, variables: Dict[str, Any]):
        super().__init__("set", variables=variables)


class SipRefer(BaseSWML):
    def __init__(self,
                 to_uri: str,
                 result: Optional[Union[dict, list]]):
        super().__init__("sip_refer", to_uri=to_uri, result=result)


class StopDenoise(BaseSWML):
    def __init__(self):
        super().__init__("stop_denoise")


class StopRecordCall(BaseSWML):
    def __init__(self,
                 control_id: Optional[str] = None):
        super().__init__("stop_record_call", control_id=control_id)


class StopTap(BaseSWML):
    def __init__(self,
                 control_id: str):
        super().__init__("stop_tap", control_id=control_id)


class Switch(BaseSWML):
    def __init__(self,
                 variable: str,
                 case: Optional[Dict[str, list]] = None,
                 default: Optional[List[Any]] = None):
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
            return {key: [x.to_dict() if isinstance(x, BaseSWML) else x for x in val] for key, val in value.items()}
        else:
            return value


class Tap(BaseSWML):
    def __init__(self,
                 uri: str,
                 control_id: Optional[str] = None,
                 direction: Optional[str] = None,
                 codec: Optional[str] = None,
                 rtp_ptime: Optional[int] = None):
        valid_directions = ["speak", "hear", "both"]
        valid_codecs = ["PCMU", "PCMA"]
        if direction and direction not in valid_directions:
            raise ValueError(f"Invalid direction. Expected one of {valid_directions}")
        if codec and codec not in valid_codecs:
            raise ValueError(f"Invalid codec. Expected one of {valid_codecs}")
        super().__init__("tap", uri=uri, control_id=control_id, direction=direction, codec=codec, rtp_ptime=rtp_ptime)


class Transfer(BaseSWML):
    def __init__(self,
                 dest: str,
                 params: Optional[Dict[str, Any]] = None,
                 meta: Optional[Dict[str, Any]] = None,
                 result: Optional[Union[dict, list]] = None):
        super().__init__("transfer", dest=dest, params=params, meta=meta, result=result)


class Unset(BaseSWML):
    def __init__(self, _vars: Union[str, List[str]]):
        super().__init__("unset", vars=_vars)
