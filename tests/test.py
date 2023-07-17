from swml import SWMLResponse, Transfer, Switch

# Create a new SWML response
response = SWMLResponse()

# Add a main_section to the response
main_section = response.add_section('main')

# Add the execute instruction to the main_section

case_dict = {
    1: [Transfer(dest="sales")],
    2: [Transfer(dest="support")],
    3: [Transfer(dest="leave_a_message")]
}

default_case = [Transfer(dest="invalid_choice")]

main_section.prompt(play='say:Please press 1 to go to sales, 2 for support, 3 to leave a message', max_digits=1)
yes = Switch(variable='prompt_value', case=case_dict, default=default_case)
main_section.add_instruction(yes)

# Add a sales section
sales_section = response.add_section('sales')
sales_section.play(url='say:This is the Sales Section.')
sales_section.hangup()


# Add a Support section
support_section = response.add_section('support')
support_section.play(url='say:This is the Support Section.')
support_section.hangup()


# Add a leave_a_message section
leave_message_section = response.add_section('leave_a_message')
leave_message_section.play(url='say:This is the leave a message section.')
leave_message_section.hangup()

# Invalid choice section
invalid_choice_section = response.add_section('invalid_choice')
invalid_choice_section.play(url='say:That was a invalid choice')
invalid_choice_section.hangup()


# Generate the SWML
swml = response.generate_swml('yaml')
print(swml)
