from openai import OpenAI
from dotenv import load_dotenv
from email.message import EmailMessage
import os
from scenario_generator import *

# Load environment variables from .env file
load_dotenv()

# Get the api key from the local environment loaded above. The OS environment variable doesn't work for me for some reason.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Mail generation function that uses the previously generated variables
def scenario_mail(scenario):

  # Set the role of the AI and the user request. The user request is quite specific in the current model.
  # For generating a high number of emails this needs to be modified.
  chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a mail content creation program. Based on the input scenario you will return an appropriate mail text welcoming the person in the scenario to the new company. First line returned should only contain the subject followed by the mail body."},
      {"role": "user", "content": f"""Scenario: {scenario}
Email: The email is from {name2} from HR at {company2} welcoming {name1} to {company2}."""}
    ]
  )

  # Just a cleaner variable for the output of the AI
  data = chat_completion.choices[0].message
  # The list that will contain the formatted data before outputting it into the mail
  datalist = []

  # Filter out the trash that comes with the AI's return and appends the output we want into our mail body list
  count = 0
  for i in data:
    if count == 0:
      datalist.append(i[1])
      count =+ 1
    else:
      pass

  # Format the data appropriately for export
  mail_list = datalist[0].split('\n')
  # Define a variable to pass data to the email generating module
  msg = EmailMessage()
  # Define a variable to contain the message body
  msg_body = ''
  count = 0
  # Set the sender and receiver of the email.
  msg['From'] = user2_email
  msg['To'] = user1_email
  # First line of the mail_list variable contains the email subject. 
  # The for loop takes the first line and sets this as the email subject. The rest is passed to a variable to contain the message body.
  for i in mail_list:
    if count == 0:
      # The way the query worded the AI always returns the subject starting with "Subject:". This if statement is put in to check if that is present and remove it if it is.
      if "Subject: " in i:
        i = i.replace("Subject: ", "")
        msg['Subject'] = i
        subject = i
      else:
        msg['Subject'] = i
      count += 1
    else:
      msg_body += i + '\n'
  # Pass the message body to the mail variable defined 
  msg.set_content(msg_body)

  # Define the filename and path
  filename = 'Email AI\original_mail.eml'

  # Save the email message to a file
  with open(filename, 'w') as eml_file:
      eml_file.write(msg.as_string())
  # Return a tuple containing the email message and email subject
  return subject, msg_body


scenario_mail(scenario_gen())