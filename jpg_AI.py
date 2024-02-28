from PIL import Image
import uuid
import os
import random

def jpg_generator(directory):
    width, height = 100, 100
    filename = str(uuid.uuid4())[:8]
    file_path = os.path.join(directory, f"{filename}.jpg")
    img = Image.new("RGB", (width, height), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    img.save(file_path)

if __name__ == '__main__':
    jpg_generator()