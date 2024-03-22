from openai import OpenAI
from dotenv import load_dotenv
from email.message import EmailMessage
import os
from scenario_mail import *
from scenario_generator import *

# Load environment variables from .env file
load_dotenv()

# Get the api key from the local environment loaded above. The OS environment variable doesn't work for me for some reason.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Mail reply function which takes the tuple returned from scenario_mail function in scenario_mail.py.
# The tuple contains the subject first and the body text of the previous email in the second entry.
def mail_reply(the_mail):

    # Set the role of the AI and pass it the body of text from the previous email as the user input. 
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a mail responding program. Carefully read the input mail and create an appropriate response. Only return the response text."},
        {"role": "user", "content": f"{the_mail[1]}"}
    ]
    )

    # Just a cleaner variable for the output of the AI
    data = chat_completion.choices[0].message
    # The list that will contain the formatted data before outputting into a content file
    datalist = []

    # Filter out the trash that comes with the AI's return and append the output we want into our content list
    count = 0
    for i in data:
        if count == 0:
            datalist.append(i[1])
            count =+ 1
        else:
            pass

    # Format the data appropriately to be appended to the message body
    mail_body = datalist[0].split('\n')
    # Define a variable to pass data to the email generating module
    msg = EmailMessage()
    # Define a variable to contain the message body
    msg_body = ''
    # Add the formatted result of the prompt to the message body
    for i in mail_body:
        msg_body += i + '\n'
    count = 0
    # Append the information from the previous email to the message body for it to look more authentic
    msg_body += '\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n'
    msg_body += f'\n> From: {user1_email}\n> To: {user2_email}\n> Subject: {the_mail[0]}\n'
    formatted_old_mail = '\n'.join('> ' + line for line in the_mail[1].split('\n'))
    msg_body += f'\n{formatted_old_mail}'
    # Set the subject, sender and receiver of the email. Reverse the sender/receiver and add "RE:" to the start of the subject to look more authentic
    msg['From'] = f'{user2_email}'
    msg['To'] = f'{user1_email}'
    msg['Subject'] = f'RE: {the_mail[0]}'
    # Pass the message body to the mail variable defined 
    msg.set_content(msg_body)

    # Define the filename and path
    filename = 'Email AI\mail_reply.eml'

    # Save the email message to a .eml file
    with open(filename, 'w') as eml_file:
        eml_file.write(msg.as_string())

mail_reply(scenario_mail(scenario))