import random
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

#Default model
model_version = "gpt-3.5-turbo"

def txt_generator(directory, prompt):
    # Picks a random function from the available in the function list and runs it.
    # The result of the function gets stored in the text variable
    prompt_list = [internal_memo, note_to_self]
    selected_prompt = random.choice(prompt_list)
    text: str = selected_prompt(prompt)
    
    # Creates the filename of the file based on the context of the text variable
    title = make_title(text)
    
    file_path = os.path.join(directory, f"{title}.txt")
    
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(text)
    
    return text, title


def internal_memo(prompt, model_version = model_version) -> str:
    chat_completion = client.chat.completions.create(
    model=model_version,
    messages=[
        {"role": "system", "content": "You are a internal memo creation program. Your only purpose is to generate generic memo data. "},
        {"role": "user", "content": f"""Your only purpose is to make internal memos that could be found on post-it notes on the desk of an employee of a big tech company.
                                       It should include a reference to who the message is for and a signature from the sender at the bottom with the format '--name 
                                       and it should have a general theme of {prompt}"""}
    ]
    )
    memo = chat_completion.choices[0].message.content
    return memo

def note_to_self(prompt, model_version = model_version) -> str:
    chat_completion = client.chat.completions.create(
    model=model_version,
    messages=[
        {"role": "system", "content": "You are a self reminder note creation program. Your only purpose is to generate believable notes written to one selves. "},
        {"role": "user", "content": f"""Your only purpose is to make small notes that might have been written as a reminder to yourself,
                                       that may be written on a post-it note or in a text file on the notepad app on your computer.
                                       The should be themed around {prompt}"""}
    ]
    )
    note = chat_completion.choices[0].message.content
    return note

def make_title(text:str) -> str:
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """You are an text summarizer.
                                         Your only task is to summarize the internal memo provided in the user prompt.
                                         You should summarize it to a title of 1-3 words that should describe the content."""},
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