from openai import OpenAI
from dotenv import load_dotenv
from generator_functions import *
import os

# Load environment variables from .env file
load_dotenv()

# Get the api key from the local environment loaded above. The OS environment variable doesn't work for me for some reason.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define the filename for a log of names, usernames, emails and scenario
data_file = "Email AI\data_file.txt"
# Generate names and tech company names for the scenario. name2 will be used for the email generator to have a receiver of the email
name1 = name_gen()
name2 = name_gen()
company1 = tech_name()
company2 = tech_name()

# Function that takes a name and two company names for the scenario generation
def scenario_gen():
    chat_completion = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-1106:applied-data-science-student:techipscenario:91F3ClD4",
    messages=[
        {"role": "system", "content": "Your task is to create a fictitious case overview for a case involving possible theft of intellectual property in the tech industry."},
        {"role": "user", "content": f"Create a scenario with the suspect {name1}, and companies {company1} and {company2}."}
    ]
    )

    return chat_completion.choices[0].message.content

# Run the scenario generator
scenario = scenario_gen()
# Create appropriate email addresses and usernames based on names and company names
company1_domain = email_domain(company1)
company2_domain = email_domain(company2)
user1_email = username(name1)+company1_domain
user2_email = username(name2)+company2_domain

with open(data_file, "w") as data:
    data.write(f"Name: {name1}\n")
    data.write(f"User email: {user1_email}\n")
    data.write("\n")
    data.write(f"Name#2: {name2}\n")
    data.write(f"User email: {user2_email}\n")
    data.write("\n")
    data.write(f"Former company: {company1}\n")
    data.write(f"Domain: {company1_domain}\n")
    data.write("\n")
    data.write(f"Current company: {company2}\n")
    data.write(f"Domain: {company2_domain}\n")
    data.write("\n")
    data.write(f"\n")
    data.write(f"Scenario: {scenario} \n")

