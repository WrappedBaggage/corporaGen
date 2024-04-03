from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def png_generator(filename, directory, prompt):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    try:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            generated_image_filename = f"{filename}.png"
            with open(os.path.join(directory, generated_image_filename), 'wb') as image_file:
                image_file.write(image_response.content)
            print(f"Image successfully saved to {os.path.join(directory, generated_image_filename)}")
            return generated_image_filename
        else:
            print(f"Failed to download image from {image_url}")
    except Exception as download_error:
        print(f"An error occurred while downloading the image: {download_error}")

if __name__ == '__main__':
    png_generator("test", "test", "Cake")