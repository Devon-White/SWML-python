# main.py

from swml_response import SWMLResponse

response = SWMLResponse()

response.answer()
response.play(url="test.com")
response.record(stereo=True)
response.hangup()

print(response.to_json())






