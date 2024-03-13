import random
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def txt_generator(directory: str):
    # Picks a random function from the available in the function list and runs it.
    # The result of the function gets stored in the text variable
    function_list = [internal_memo, note_to_self]
    selected_function = random.choice(function_list)
    text: str = selected_function()
    
    # Creates the filename of the file based on the context of the text variable
    title = make_title(text)
    
    file_path = os.path.join(directory, f"{title}.txt")
    
    with open(file_path, 'w') as file:
        file.write(text)
    
    return text, title


def internal_memo() -> str:
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a internal memo creation program. Your only purpose is to generate generic memo data. "},
        {"role": "user", "content": """Your only purpose is to make internal memos that could be found on post-it notes on the desk of an employee of a big tech company.
                                       It should include a reference to who the message is for and a signature from the sender at the bottom with the format '--name"""}
    ]
    )
    memo = chat_completion.choices[0].message.content
    return memo

def note_to_self() -> str:
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a self reminder note creation program. Your only purpose is to generate believable notes written to one selves. "},
        {"role": "user", "content": """Your only purpose is to make small notes that might have been written as a reminder to yourself,
                                       that may be written on a post-it note or in a text file on the notepad app on your computer."""}
    ]
    )
    note = chat_completion.choices[0].message.content
    print(note)
    return note

def make_title(text:str) -> str:
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """You are an internal memo summarizer.
                                         Your only task is to summarize the internal memo provided in the user prompt.
                                         You should summarize it to a title of 1-3 words that should describe the memo's content."""},
        {"role": "user", "content": text}
    ]
    )
    filename = chat_completion.choices[0].message.content
    return filename
    
if __name__ == '__main__':
    directory = "txt_test"
    if not os.path.exists(directory):
        os.makedirs(directory)
    txt_generator(directory)