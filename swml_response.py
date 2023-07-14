# swml_response.py

import json
from swml_methods import *
from swml_statements import *


def add_element(self, element):
    if not hasattr(element, "to_dict"):
        raise ValueError("element must have a to_dict method")
    self.elements.append(element)

class SWMLResponse:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        if not hasattr(element, "to_dict"):
            raise ValueError("element must have a to_dict method")
        self.elements.append(element)


    # In SWMLResponse class
    def to_json(self):
        sections = {"sections": {"main": []}}
        no_parameter_methods = ['answer', 'hangup', 'denoise', 'stopdenoise', 'receivefax', 'stoptap', 'record']
        for element in self.elements:
            method_name = element.__class__.__name__.lower()
            element_dict = element.to_dict()

            if method_name in no_parameter_methods:
                if element_dict and not isinstance(element_dict, str):
                    sections["sections"]["main"].append({method_name: element_dict})
                else:
                    sections["sections"]["main"].append(method_name)
            elif method_name == 'play':
                if isinstance(element_dict, str) or (
                        isinstance(element_dict, dict) and "urls" in element_dict and len(element_dict["urls"]) == 1):
                    sections["sections"]["main"].append({method_name: element_dict})
                else:
                    sections["sections"]["main"].append({method_name: {"urls": element_dict}})
            else:
                sections["sections"]["main"].append({method_name: element_dict})

        # Remove the empty dictionaries for methods with no parameters
        sections["sections"]["main"] = [item for item in sections["sections"]["main"] if item]

        return json.dumps(sections, indent=4)

    def __str__(self):
        return self.to_json()

    # Methods
    def answer(self,
               max_duration=None):
        self.add_element(Answer(max_duration))

    def hangup(self, reason=None):
        self.add_element(Hangup(reason))

    def prompt(self,
               play,
               volume=None,
               say_voice=None,
               say_language=None,
               say_gender=None,
               max_digits=None,
               terminators=None,
               digit_timeout=None,
               initial_timeout=None,
               speech_timeout=None,
               speech_end_timeout=None,
               speech_language=None,
               speech_hints=None):
        self.add_element(Prompt(play,
                                volume,
                                say_voice,
                                say_language,
                                say_gender,
                                max_digits,
                                terminators,
                                digit_timeout,
                                initial_timeout,
                                speech_timeout,
                                speech_end_timeout,
                                speech_language,
                                speech_hints))

    def play(self,
             url=None,
             urls=None,
             volume=None,
             say=None,
             silence=None,
             ring=None):


        self.add_element(Play(url, urls, volume, say, silence, ring))

    def record(self,
               stereo=None,
               format=None,
               direction=None,
               terminators=None,
               beep=None,
               input_sensitivity=None,
               initial_timeout=None,
               end_silence_timeout=None):
        self.add_element(Record(stereo, format, direction, terminators, beep, input_sensitivity, initial_timeout, end_silence_timeout))

    def record_call(self,
                    control_id=None,
                    stereo=None,
                    format=None,
                    direction=None,
                    terminators=None,
                    beep=None,
                    input_sensitivity=None,
                    initial_timeout=None,
                    end_silence_timeout=None):
        self.add_element(RecordCall(control_id, stereo, format, direction, terminators, beep, input_sensitivity, initial_timeout, end_silence_timeout))

    def stop_record_call(self, control_id=None):
        self.add_element(StopRecordCall(control_id))

    def join_room(self, name):
        self.add_element(JoinRoom(name))

    def denoise(self):
        self.add_element(Denoise())

    def stop_denoise(self):
        self.add_element(StopDenoise())

    def receive_fax(self):
        self.add_element(ReceiveFax())

    def send_fax(self, document, header_info=None, identity=None):
        self.add_element(SendFax(document, header_info, identity))

    def sip_refer(self, to_uri):
        self.add_element(SipRefer(to_uri))

    def connect(self,
                from_=None,
                headers=None,
                codecs=None,
                webrtc_media=None,
                session_timeout=None,
                ringback=None,
                serial_parallel=None,
                serial=None,
                parallel=None,
                to=None):
        self.add_element(Connect(from_, headers, codecs, webrtc_media, session_timeout, ringback, serial_parallel, serial, parallel, to))

    # Statements
    def transfer(self, dest, params=None, meta=None):
        self.add_element(Transfer(dest, params, meta))

    def execute(self, dest, params=None, on_return=None):
        self.add_element(Execute(dest, params, on_return))

    def return_(self, return_value=None):
        self.add_element(Return(return_value))

    def request(self, url, method, headers=None, body=None, timeout=5.0, connect_timeout=5.0, save_variables=False):
        self.add_element(Request(url, method, headers, body, timeout, connect_timeout, save_variables))

    def switch(self, variable, case=None, default=None):
        self.add_element(Switch(variable, case, default))

    def cond(self, when, then, else_):
        self.add_element(Cond(when, then, else_))

    def set(self, variables):
        self.add_element(Set(variables))

    def unset(self, vars):
        self.add_element(Unset(vars))