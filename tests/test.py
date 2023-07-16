from swml import SWMLResponse, Transfer, Switch

# Create a new SWML response
response = SWMLResponse()

# Add a main_section to the response
main_section = response.add_section('main')

# Add the execute instruction to the main_section
execute_params = {
    "file": "https://example.com/foo.wav",
    "digits": "123"
}
case_dict = {
    1: [Transfer(dest="sales")],
    2: [Transfer(dest="support")],
    3: [Transfer(dest="leave_a_message")]
}

default_case = [Transfer(dest="invalid_choice")]

execute_on_return = [Switch(variable="return_value", case=case_dict, default=default_case)]
main_section.execute(dest="my_menu", params=execute_params, on_return=execute_on_return)

# Add a subroutine_section to the response
subroutine_section = response.add_section('subroutine')

# Add the answer instruction to the subroutine_section
subroutine_section.answer()

# Generate the SWML
swml = response.generate_swml('yaml')
print(swml)
