from openai import OpenAI
from dotenv import load_dotenv
from email.message import EmailMessage
import os
import re

# Load environment variables from .env file
load_dotenv()

# Gets the api key from the local environment loaded above. The OS environment variable doesn't work for me for some reason.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def mail_generator(filename, directory):
    # Set the role of the AI and the user request
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a mail content creation program. Your only purpose is to generate generic mail data. "},
        {"role": "user", "content": "Create content for a mail that could be found on the laptop of an employee of a big tech company. You decide on an appropriate context. The following conditions are very important! First line should contain a mail address, second line should contain a mail address, third line should contain a subject, and the rest should be the contents of the mail, and names need to be made up. The first three lines cannot contain 'to', 'from' or 'subject'"}
    ]
    )

    # Just a cleaner variable for the output of the AI
    data = chat_completion.choices[0].message
    # The list that will contain the formatted data before outputting into a CSV file
    datalist = []

    # Filters out the trash that comes with the AI's return and appends the output we want into our CSV list
    count = 0
    for i in data:
        if count == 0:
            datalist.append(i[1])
            count =+ 1
        else:
            pass

    # Formats the data appropriately for CSV export
    mail_list = datalist[0].split('\n')

    msg = EmailMessage()
    msg_body = ''
    count = 0

    for i in mail_list:
        if count == 0:
            msg['From'] = i
            count += 1
        elif count == 1:
            msg['To'] = i
            count += 1
        elif count == 2:
            msg['Subject'] = i
            count += 1
        else:
            msg_body += i + '\n'

    msg.set_content(msg_body)

    # Define the filename and path
    subject = msg['Subject']
    filename = re.sub(r'\W+', '_', subject)
    file_path = os.path.join(directory, f"{filename}.eml")

    # Save the email message to a file
    with open(file_path, 'w') as eml_file:
        eml_file.write(msg.as_string())

if __name__ == '__main__':
    mail_generator()