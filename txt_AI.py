from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def txt_generator(filename, directory):
    # Creates the text of the file
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a internal memo creation program. Your only purpose is to generate generic memo data. "},
        {"role": "user", "content": "Your only purpose is to make internal memos that could be found on post-it notes on the desk of an employee of a big tech company. It should include a reference to who the message is for and a signature from the sender at the bottom with the format '--name"}
    ]
    )
    text = chat_completion.choices[0].message.content
    
    # Creates the title of the file
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an internal memo summarizer. Your only task is to summarize the internal memo provided in the user prompt. You should summarize it to a title of 1-3 words that should describe the memo's content."},
        {"role": "user", "content": text}
    ]
    )
    filename = chat_completion.choices[0].message.content
    
    file_path = os.path.join(directory, f"{filename}.txt")
    
    with open(file_path, 'w') as file:
        file.write(text)
    
    return text

if __name__ == '__main__':
    txt_generator("test", "")