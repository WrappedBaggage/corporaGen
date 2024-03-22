from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Gets the api key from the local environment loaded above. The OS environment variable doesn't work for me for some reason.
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def name_gen():
    chat_completion = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-1106:applied-data-science-student:random-namev2:8yt23vqe",
    messages=[
        {"role": "system", "content": "You're a random name generator that only returns a random name upon request."},
        {"role": "user", "content": "Generate a name."}
        ]
    )
    return chat_completion.choices[0].message.content

def tech_name():
    completion = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:applied-data-science-student:my-suffix:8yrMK3ZO",
    messages=[
        {"role": "system", "content": "You're a creative random tech company name generator."},
        {"role": "user", "content": "Generate a tech company name."}
        ]
    )
    return completion.choices[0].message.content

def email_domain(input):
    completion = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:applied-data-science-student:email-creatorv2:8yuDHZlm",
    messages=[
        {"role": "system", "content": "You're an email address generator based on a company name input, which only returns everything after, and including, the '@' symbol."},
        {"role": "user", "content": f"{input}"}
        ]
    )
    return completion.choices[0].message.content

def username(name):
    name = name.replace(" ", "")
    name = name.lower()

    return name